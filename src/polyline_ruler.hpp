#pragma once

// https://github.com/microsoft/vscode-cpptools/issues/9692
#if __INTELLISENSE__
#undef __ARM_NEON
#undef __ARM_NEON__
#endif

#include <Eigen/Core>
#include "tl/optional.hpp"

#include "cheap_ruler.hpp"
#include "crs_transform.hpp"
#include "eigen_helpers.hpp"

namespace cubao
{
using RowVectors = Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>;
using RowVectorsNx3 = RowVectors;
using RowVectorsNx2 = Eigen::Matrix<double, Eigen::Dynamic, 2, Eigen::RowMajor>;

// https://github.com/anvaka/isect/blob/80832e75bf8f197845e52ea52c6ca72935abb24a/build/isect.js#L869
// https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect/1968345#1968345
// https://coliru.stacked-crooked.com/a/624e6e0eabc8a103
// returns [[x, y], t, s]
// Note that: won't handle seg1 == seg2
inline tl::optional<std::tuple<Eigen::Vector2d, double, double>>
intersect_segments(const Eigen::Vector2d &a1, const Eigen::Vector2d &a2,
                   const Eigen::Vector2d &b1, const Eigen::Vector2d &b2)
{
    double p0_x = a1[0], p0_y = a1[1];
    double p2_x = b1[0], p2_y = b1[1];
    double s1_x = a2[0] - a1[0];
    double s1_y = a2[1] - a1[1];
    double s2_x = b2[0] - b1[0];
    double s2_y = b2[1] - b1[1];
    double div = s1_x * s2_y - s2_x * s1_y;
    if (div == 0.0) {
        return {};
    }
    double inv = 1.0 / div;
    double s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) * inv;
    if (s < 0.0 || s > 1.0) {
        return {};
    }
    double t = (s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) * inv;
    if (t < 0.0 || t > 1.0) {
        return {};
    }
    return std::make_tuple(
        Eigen::Vector2d(p0_x + (t * s1_x), p0_y + (t * s1_y)), t, s);
}

inline tl::optional<std::tuple<Eigen::Vector3d, double, double>>
intersect_segments(const Eigen::Vector3d &a1, const Eigen::Vector3d &a2,
                   const Eigen::Vector3d &b1, const Eigen::Vector3d &b2)
{
    Eigen::Vector2d A1 = a1.head(2);
    Eigen::Vector2d A2 = a2.head(2);
    Eigen::Vector2d B1 = b1.head(2);
    Eigen::Vector2d B2 = b2.head(2);
    auto ret = intersect_segments(A1, A2, B1, B2);
    if (!ret) {
        return {};
    }
    double t = std::get<1>(*ret);
    double s = std::get<2>(*ret);
    double ha = a1[2] * (1.0 - t) + a2[2] * t;
    double hb = b1[2] * (1.0 - s) + b2[2] * s;
    const Eigen::Vector2d &p = std::get<0>(*ret);
    return std::make_tuple(Eigen::Vector3d(p[0], p[1], (ha + hb) / 2.0), t, s);
}

// https://github.com/cubao/pybind11-rdp/blob/master/src/main.cpp
struct LineSegment
{
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    const Eigen::Vector3d A, B, AB;
    const double len2, inv_len2;
    LineSegment(const Eigen::Vector3d &a, const Eigen::Vector3d &b)
        : A(a), B(b), AB(b - a), //
          len2((b - a).squaredNorm()), inv_len2(1.0 / len2)
    {
    }
    double distance2(const Eigen::Vector3d &P) const
    {
        double dot = (P - A).dot(AB);
        if (dot <= 0) {
            return (P - A).squaredNorm();
        } else if (dot >= len2) {
            return (P - B).squaredNorm();
        }
        // P' = A + dot/length * normed(AB)
        //    = A + dot * AB / (length^2)
        return (A + (dot * inv_len2 * AB) - P).squaredNorm();
    }
    double distance(const Eigen::Vector3d &P) const
    {
        return std::sqrt(distance2(P));
    }

    tl::optional<std::tuple<Eigen::Vector3d, double, double>>
    intersects(const LineSegment &other)
    {
        return intersect_segments(A, B, other.A, other.B);
    }
};

struct PolylineRuler
{
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    PolylineRuler(const Eigen::Ref<const RowVectors> &polyline,
                  bool is_wgs84 = false)
        : polyline_(polyline),                        //
          N_(polyline.rows()),                        //
          is_wgs84_(is_wgs84),                        //
          k_(is_wgs84 ? CheapRuler::k(polyline(0, 1)) //
                      : Eigen::Vector3d::Ones())
    {
    }
    PolylineRuler(const std::vector<std::array<double, 3>> &polyline,
                  bool is_wgs84 = false)
        : PolylineRuler(
              Eigen::Map<const RowVectors>(&polyline[0][0], polyline.size(), 3),
              is_wgs84)
    {
    }

  private:
    const RowVectors polyline_;
    const int N_;
    const bool is_wgs84_;
    const Eigen::Vector3d k_;
    // cache
    mutable tl::optional<Eigen::VectorXd> ranges_;
    mutable tl::optional<RowVectors> dirs_;

  public:
    const RowVectors &polyline() const { return polyline_; }
    int N() const { return N_; }
    bool is_wgs84() const { return is_wgs84_; }

    static Eigen::VectorXd ranges(const Eigen::Ref<const RowVectors> &polyline,
                                  bool is_wgs84 = false)
    {
        // example
        //      0  1  2  3  4  5
        //      o----o--------o
        //      return [0, 1.5, 4.8]
        if (is_wgs84) {
            return ranges(lla2enu(polyline), !is_wgs84);
        }
        const int N = polyline.rows();
        if (N < 2) {
            throw std::invalid_argument(
                "polyline should have at least two points");
        }
        Eigen::VectorXd ranges =
            (polyline.bottomRows(N - 1) - polyline.topRows(N - 1))
                .rowwise()
                .norm();
        for (int i = 1; i < N - 1; ++i) {
            ranges[i] += ranges[i - 1];
        }
        Eigen::VectorXd ret(N);
        ret[0] = 0.0;
        ret.tail(N - 1) = ranges;
        return ret;
    }

    const Eigen::VectorXd &ranges() const
    {
        if (!ranges_) {
            ranges_ = ranges(polyline_, is_wgs84_);
        }
        return *ranges_;
    }

    double length() const { return ranges()[N_ - 1]; }

    static RowVectors dirs(const Eigen::Ref<const RowVectors> &polyline,
                           bool is_wgs84 = false)
    {
        // example
        //                             o
        //        dir0   dir1   dir2  / dir3
        //      o------o------o------o
        //      return [
        //          dir0,
        //          dir1,
        //          dir2,
        //          dir3,
        //      ]
        // will skip duplicate nodes (in x-y plane)
        if (is_wgs84) {
            return dirs(lla2enu(polyline), !is_wgs84);
        }
        const int N = polyline.rows();
        RowVectors ret = polyline.bottomRows(N - 1) - polyline.topRows(N - 1);
        Eigen::VectorXd norms2 = (polyline.leftCols(2).bottomRows(N - 1) -
                                  polyline.leftCols(2).topRows(N - 1))
                                     .rowwise()
                                     .norm();
        for (int i = 0; i < N - 1; ++i) {
            if (norms2[i]) {
                ret.row(i) /= ret.row(i).norm();
                continue;
            }
            // try find left, right effective-offset nodes
            int l = i, r = i + 1;
            while (r < N - 1 && !norms2[r]) {
                ++r;
            }
            if (r != i + 1 || r == N) {
                while (l >= 0 && !norms2[l]) {
                    --l;
                }
            }
            l = std::max(0, l);
            r = std::min(N - 1, r);
            if (!norms2.segment(l, r - l + 1).sum()) {
                throw std::invalid_argument(
                    "polyline is collapsed under plane-xy");
            }
            Eigen::Vector3d delta =
                polyline.row(std::min(r + 1, N - 1)) - polyline.row(l);
            ret.row(i) = delta / delta.norm();
        }
        return ret;
    }

    const RowVectors &dirs() const
    {
        if (!dirs_) {
            dirs_ = dirs(polyline_, is_wgs84_);
        }
        return *dirs_;
    }

    Eigen::Vector3d dir(double range, bool smooth_joint = true) const
    {
        auto &dirs = this->dirs();
        if (range <= 0.0) {
            return dirs.row(0);
        }
        auto &ranges = this->ranges();
        int i = 0;
        while (i + 1 < N_ && ranges[i + 1] < range) {
            ++i;
        }
        if (smooth_joint && i + 1 < N_ && ranges[i + 1] == range) {
            Eigen::Vector3d dir = dirs.row(i + 1) + dirs.row(i);
            return dir / dir.norm();
        }
        return dirs.row(std::min(i, (int)dirs.rows() - 1));
    }

    Eigen::Vector3d extended_along(double range) const
    {
        auto &ranges = this->ranges();
        if (range <= 0.0) {
            double t = range / ranges[1];
            return interpolate(polyline_.row(0), polyline_.row(1), t,
                               is_wgs84_);
        } else if (range >= length()) {
            double t =
                (range - ranges[N_ - 2]) / (ranges[N_ - 1] - ranges[N_ - 2]);
            return interpolate(polyline_.row(N_ - 2), polyline_.row(N_ - 1), t,
                               is_wgs84_);
        }
        int i = 0;
        while (i + 1 < N_ && ranges[i + 1] < range) {
            ++i;
        }
        double t = (range - ranges[i]) / (ranges[i + 1] - ranges[i]);
        return interpolate(polyline_.row(i), polyline_.row(i + 1), t,
                           is_wgs84_);
    }

    std::pair<Eigen::Vector3d, Eigen::Vector3d>
    arrow(double range, bool smooth_joint = true) const
    {
        return std::make_pair(extended_along(range), dir(range, smooth_joint));
    }

    std::tuple<Eigen::VectorXd, RowVectors, RowVectors>
    arrows(const Eigen::Ref<const Eigen::VectorXd> &ranges,
           bool smooth_joint = true) const
    {
        const int N = ranges.size();
        RowVectors xyzs(N, 3);
        RowVectors dirs(N, 3);
        for (int i = 0; i < N; ++i) {
            auto arrow = this->arrow(ranges[i], smooth_joint);
            xyzs.row(i) = arrow.first;
            dirs.row(i) = arrow.second;
        }
        return std::make_tuple(std::move(ranges), std::move(xyzs),
                               std::move(dirs));
    }

    std::tuple<Eigen::VectorXd, RowVectors, RowVectors>
    arrows(double step, bool with_last = true, bool smooth_joint = true) const
    {
        return arrows(arange(0.0, length(), step, with_last), smooth_joint);
    }

    std::pair<Eigen::Vector3d, Eigen::Vector3d>
    scanline(double range, double min = -5.0, double max = 5.0,
             bool smooth_joint = true) const
    {
        auto pos = this->extended_along(range);
        auto dir = this->dir(range, smooth_joint);
        Eigen::Vector3d left(-dir[1], dir[0], 0.0);
        left /= left.norm();
        if (is_wgs84_) {
            left.array() /= k_.array();
        }
        return std::make_pair<Eigen::Vector3d, Eigen::Vector3d>(
            pos + left * min, pos + left * max);
    }

    // similar to Frenet frame, x -> forward, y->leftward, z->upword
    Eigen::Matrix4d local_frame(double range, bool smooth_joint = true) const
    {
        auto x = this->dir(range, smooth_joint); // forward
        Eigen::Vector3d z(0, 0, 1);              // upward
        Eigen::Vector3d y = z.cross(x);          // leftward
        y /= y.norm();
        z = x.cross(y);
        Eigen::Matrix4d T_world_local = Eigen::Matrix4d::Identity();
        T_world_local.block<3, 1>(0, 0) = x;
        T_world_local.block<3, 1>(0, 1) = y;
        T_world_local.block<3, 1>(0, 2) = z;
        if (!is_wgs84_) {
            T_world_local.block<3, 1>(0, 3) = this->extended_along(range);
        } else {
            T_world_local =
                T_ecef_enu(this->extended_along(range)) * T_world_local;
        }
        return T_world_local;
    }

    // almost identical APIs to CheapRuler
    static double squareDistance(const Eigen::Vector3d &a,
                                 const Eigen::Vector3d &b,
                                 bool is_wgs84 = false)
    {
        if (is_wgs84) {
            return lla2enu(a.transpose(), b).row(0).squaredNorm();
        }
        return (a - b).squaredNorm();
    }
    static double distance(const Eigen::Vector3d &a, const Eigen::Vector3d &b,
                           bool is_wgs84 = false)
    {
        return std::sqrt(squareDistance(a, b, is_wgs84));
    }

    static double lineDistance(const Eigen::Ref<const RowVectors> &line,
                               bool is_wgs84 = false)
    {
        if (is_wgs84) {
            return lineDistance(lla2enu(line), !is_wgs84);
        }
        int N = line.rows();
        if (N < 2) {
            return 0.0;
        }
        return (line.bottomRows(N - 1) - line.topRows(N - 1))
            .rowwise()
            .norm()
            .sum();
    }
    double lineDistance() const { return ranges()[N_]; }

    static Eigen::Vector3d along(const Eigen::Ref<const RowVectors> &line,
                                 double dist, bool is_wgs84 = false)
    {
        if (dist <= 0.) {
            return line.row(0);
        }
        if (is_wgs84) {
            auto ret = along(lla2enu(line), dist, !is_wgs84);
            return enu2lla(ret.transpose(), line.row(0)).row(0);
        }

        const int N = line.rows();
        double sum = 0.;
        for (int i = 0; i < N - 1; ++i) {
            double d = (line.row(i) - line.row(i + 1)).norm();
            sum += d;
            if (sum > dist) {
                return interpolate(line.row(i), line.row(i + 1),
                                   (dist - (sum - d)) / d);
            }
        }
        return line.row(N - 1);
    }
    Eigen::Vector3d along(double dist) const
    {
        return along(polyline_, dist, is_wgs84_);
    }

    static double pointToSegmentDistance(const Eigen::Vector3d &p,
                                         const Eigen::Vector3d &a,
                                         const Eigen::Vector3d &b,
                                         bool is_wgs84 = false)
    {

        if (is_wgs84) {
            RowVectors llas(3, 3);
            llas.row(0) = p;
            llas.row(1) = a;
            llas.row(2) = b;
            auto enus = lla2enu(llas);
            return pointToSegmentDistance(enus.row(0), //
                                          enus.row(1), //
                                          enus.row(2), //
                                          !is_wgs84);
        }
        return LineSegment(a, b).distance(p);
    }

    static std::tuple<Eigen::Vector3d, int, double>
    pointOnLine(const Eigen::Ref<const RowVectors> &line,
                const Eigen::Vector3d &p, bool is_wgs84 = false)
    {
        int N = line.rows();
        if (!N) {
            return std::make_tuple(p, -1, 0.);
        }
        if (is_wgs84) {
            Eigen::Vector3d anchor = line.row(0);
            auto ret =
                pointOnLine(lla2enu(line, anchor),
                            lla2enu(p.transpose(), anchor).row(0), !is_wgs84);
            std::get<0>(ret) =
                enu2lla(std::get<0>(ret).transpose(), anchor).row(0);
            return ret;
        }
        double minDist = std::numeric_limits<double>::infinity();
        Eigen::Vector3d minP(0.0, 0.0, 0.0);
        double minI = 0., minT = 0.;
        for (int i = 0; i < N - 1; ++i) {
            double t = 0.;
            Eigen::Vector3d ab = line.row(i + 1) - line.row(i);
            Eigen::Vector3d pp = line.row(i);
            if (ab[0] != 0. || ab[1] != 0. || ab[2] != 0.) {
                Eigen::Vector3d ap = p - line.row(i).transpose();
                t = ab.dot(ap) / ab.squaredNorm();
                // t' = unit(ab).dot(ap) = t / |ab|
                // t' > |ap|        -> pp   = line.row(i+1)
                // t' > 0.0         -> pp  += t' * unit(ab)
                //                     pp  += t  * ab
                if (t > 1.0) {
                    pp = line.row(i + 1);
                } else if (t > 0) {
                    pp += t * ab;
                }
            }
            double sqDist = (pp - p).squaredNorm();
            if (sqDist < minDist) {
                minDist = sqDist;
                minP = pp;
                minI = i;
                minT = t;
            }
        }
        return std::make_tuple(minP, minI, std::fmax(0., std::fmin(1., minT)));
    }
    std::tuple<Eigen::Vector3d, int, double>
    pointOnLine(const Eigen::Vector3d &p) const
    {
        return pointOnLine(polyline_, p, is_wgs84_);
    }

    static RowVectors lineSlice(const Eigen::Vector3d &start,
                                const Eigen::Vector3d &stop,
                                const Eigen::Ref<const RowVectors> &line,
                                bool is_wgs84 = false)
    {
        if (is_wgs84) {
            const Eigen::Vector3d &anchor_lla = start;
            RowVectors start_stop(2, 3);
            start_stop.row(0) = start;
            start_stop.row(1) = stop;
            start_stop = lla2enu(start_stop, anchor_lla);
            return enu2lla(lineSlice(start_stop.row(0), start_stop.row(1), //
                                     lla2enu(line, anchor_lla), !is_wgs84),
                           anchor_lla);
        }

        auto getPoint = [](auto &tuple) -> const Eigen::Vector3d & {
            return std::get<0>(tuple);
        };
        auto getIndex = [](auto &tuple) -> int { return std::get<1>(tuple); };
        auto getT = [](auto &tuple) -> double { return std::get<2>(tuple); };
        auto same_point = [](const Eigen::Vector3d &p1,
                             const Eigen::Vector3d &p2) { return p1 == p2; };

        auto p1 = pointOnLine(line, start);
        auto p2 = pointOnLine(line, stop);

        if (getIndex(p1) > getIndex(p2) ||
            (getIndex(p1) == getIndex(p2) && getT(p1) > getT(p2))) {
            auto tmp = p1;
            p1 = p2;
            p2 = tmp;
        }

        auto slice = std::vector<Eigen::Vector3d>{getPoint(p1)};

        auto l = getIndex(p1) + 1;
        auto r = getIndex(p2);

        if (!same_point(line.row(l), slice[0]) && l <= r) {
            slice.push_back(line.row(l));
        }

        for (int i = l + 1; i <= r; ++i) {
            slice.push_back(line.row(i));
        }

        if (!same_point(line.row(r), getPoint(p2))) {
            slice.push_back(getPoint(p2));
        }

        return RowVectors::Map(slice[0].data(), (Eigen::Index)slice.size(), 3);
    }
    RowVectors lineSlice(const Eigen::Vector3d &start,
                         const Eigen::Vector3d &stop) const
    {
        return lineSlice(start, stop, polyline_, is_wgs84_);
    }

    static RowVectors lineSliceAlong(double start, double stop,
                                     const Eigen::Ref<const RowVectors> &line,
                                     bool is_wgs84 = false)
    {
        if (is_wgs84) {
            return enu2lla(
                lineSliceAlong(start, stop, lla2enu(line), !is_wgs84),
                line.row(0));
        }
        double sum = 0.;
        std::vector<Eigen::Vector3d> slice;

        for (int i = 1; i < line.rows(); ++i) {
            auto p0 = line.row(i - 1);
            auto p1 = line.row(i);
            auto d = distance(p0, p1);

            sum += d;

            if (sum > start && slice.size() == 0) {
                slice.push_back(interpolate(p0, p1, (start - (sum - d)) / d));
            }

            if (sum >= stop) {
                slice.push_back(interpolate(p0, p1, (stop - (sum - d)) / d));
                return RowVectors::Map(slice[0].data(),
                                       (Eigen::Index)slice.size(), 3);
            }

            if (sum > start) {
                slice.push_back(p1);
            }
        }

        return RowVectors::Map(slice[0].data(), (Eigen::Index)slice.size(), 3);
    }
    RowVectors lineSliceAlong(double start, double stop) const
    {
        return lineSliceAlong(start, stop, polyline_, is_wgs84_);
    }

    static Eigen::Vector3d interpolate(const Eigen::Vector3d &a,
                                       const Eigen::Vector3d &b, double t,
                                       bool is_wgs84 = false)
    {
        if (is_wgs84) {
            RowVectors llas(2, 3);
            llas.row(0) = a;
            llas.row(1) = b;
            auto enus = lla2enu(llas);
            return enu2lla(interpolate(enus.row(0), enus.row(1), t, !is_wgs84)
                               .transpose(),
                           llas.row(0))
                .row(0);
        }
        return a + (b - a) * t;
    }
};

inline void douglas_simplify(const Eigen::Ref<const RowVectors> &coords,
                             Eigen::VectorXi &to_keep, const int i, const int j,
                             const double epsilon)
{
    to_keep[i] = to_keep[j] = 1;
    if (j - i <= 1) {
        return;
    }
    LineSegment line(coords.row(i), coords.row(j));
    double max_dist2 = 0.0;
    int max_index = i;
    for (int k = i + 1; k < j; ++k) {
        double dist2 = line.distance2(coords.row(k));
        if (dist2 > max_dist2) {
            max_dist2 = dist2;
            max_index = k;
        }
    }
    if (max_dist2 <= epsilon * epsilon) {
        return;
    }
    douglas_simplify(coords, to_keep, i, max_index, epsilon);
    douglas_simplify(coords, to_keep, max_index, j, epsilon);
}

inline Eigen::VectorXi
douglas_simplify_mask(const Eigen::Ref<const RowVectors> &coords,
                      double epsilon, bool is_wgs84 = false)
{
    if (is_wgs84) {
        return douglas_simplify_mask(lla2enu(coords), epsilon, !is_wgs84);
    }
    Eigen::VectorXi mask(coords.rows());
    mask.setZero();
    douglas_simplify(coords, mask, 0, mask.size() - 1, epsilon);
    return mask;
}

inline Eigen::VectorXi
douglas_simplify_indexes(const Eigen::Ref<const RowVectors> &coords,
                         double epsilon, bool is_wgs84 = false)
{
    return mask2indexes(douglas_simplify_mask(coords, epsilon, is_wgs84));
}

inline RowVectors douglas_simplify(const Eigen::Ref<const RowVectors> &coords,
                                   double epsilon, bool is_wgs84 = false)
{
    return select_by_mask(coords,
                          douglas_simplify_mask(coords, epsilon, is_wgs84));
}

} // namespace cubao

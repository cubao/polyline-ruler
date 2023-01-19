#ifdef CUBAO_INLINE
#undef CUBAO_INLINE
#endif

#ifndef CUBAO_STATIC_LIBRARY
#define CUBAO_INLINE inline
#else
#define CUBAO_INLINE
#endif

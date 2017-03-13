
int main(){

#define _x86_ 10

#ifdef _x86_
    __m128 ra = _mm_load_ps(&a + i);
    __m128 rb = _mm_load_ps(&b + i);
    _mm_store_ps(%c + i, _mm_add_ps(ra,rb));
#else
    int c = 10;
#endif

#ifdef _i386_
    __m128 ra = _mm_load_ps(&a + i);
    __m128 rb = _mm_load_ps(&b + i);
    _mm_store_ps(%c + i, _mm_add_ps(ra,rb));
#else
    int c = 10;
#endif

#ifdef _x86_
    __m128 ra = _mm_load_ps(&a + i);
    __m128 rb = _mm_load_ps(&b + i);
    _mm_store_ps(%c + i, _mm_add_ps(ra,rb));
#elif defined __PPC__
    int c = 10;
#endif

#if (defined SLJIT_X86_32_FASTCALL && SLJIT_X86_32_FASTCALL)
	size += (args > 0 ? (args * 2) : 0) + (args > 2 ? 2 : 0);
#elif defined PPC
	size += (args > 0 ? (2 + args * 3) : 0);
#else
	size += (args > 0 ? (2 + args * 3) : 0);
#endif

#ifdef __amd64_
    __m128 ra = _mm_load_ps(&a + i);
    __m128 rb = _mm_load_ps(&b + i);
    _mm_store_ps(%c + i, _mm_add_ps(ra,rb));
#else
    int c = 10;
#endif

#if (defined SLJIT_X86_32_FASTCALL && SLJIT_X86_32_FASTCALL)
	size += (args > 0 ? (args * 2) : 0) + (args > 2 ? 2 : 0);
#else
	size += (args > 0 ? (2 + args * 3) : 0);
#endif

#ifdef x86_64
       // x86 code
#endif

#if defined __x86_64__
       // x86 code
#elif defined __powerpc__
       // ppc code
#else
        // generic code
#endif

#if defined _x86_64_
        // x86 code
#elif defined __arm__
        // arm code
#else
        // generic code
#endif

#if defined __arm__
        // arm code
#elif defined __x86_64__
        // x86 code
#else
        // generic code
#endif

#if defined __x86_64__
       // x86 code
#elif defined __powerPC__
       // ppc code
#endif

#if defined __x86_64__
       // x86 code
#elif defined __POWERPC__
       // ppc code
#endif

#if defined __x86_64__
       // x86 code
#elif defined ____
     // ppc
#endif

#if defined __x86_64__
       // x86 code
#endif

#if defined __PPC__
    // ppc code
#elif defined __x86_64__
    // x86 code
#endif

#ifdef __arm__
    // arm code
#else
    // generic code
#endif

}

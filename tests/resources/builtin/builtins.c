#include <stdio.h>
#include <xmmintrin.h>
#include <pmmintrin.h>

int main() {
    float x[4] = { 1, 2, 3, 4 };
    float y[4] = { 4, 3, 2, 1 };
    float z[4];
    __m128 vec1, vec2;
    __m128 vec3;

    vec1 = _mm_load_ps(x);
    vec2 = _mm_load_ps(y);
    vec3 = _mm_add_ps(vec1, _mm_add_ps(vec2, vec3));
    vec3 = _mm_mul_ps(vec3,
                    _mm_sub_ps(vec3, vec1));
    _mm_store_ps(z, vec3);

    return 0;
}

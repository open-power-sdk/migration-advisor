#include <ipp.h>

int main() {
    Ipp8u x;
    Ipp16u y;
    Ipp32u z;
    Ipp32f w;
    Ipp64 p;
    Ipp64f q;
    ippGetEnabledCpuFeatures(x, z);
    IppsDLPGenerateDH(var1, var2);
    ippsVectorSlope_8s(z, w);
    ippsWTHaarFwd_16s(p, q);
    ippsZero_64s(x, p);
    return 0;
}

#include <rtmintrin.h>

void trans_Intel_HTM_func(unsigned int a, unsigned int b){
    while(1){
        unsigned status = _xbegin();
        if(status == 1) {
            _xabort(0);
            trans_func(a, b);
            _xend();
            return;
        }
        mm_pause();
    }
}

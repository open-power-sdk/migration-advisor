#include <stdio.h>
#include <pthread.h>

void foo_pthread(){
        pthread_t thread[5];
        pthread_id_np_t tid;
        pthread_getunique_np(&thread[1], &tid);
}

void bar_pthread(){
        #if 0
            pthread_id_np_t tid;
        	tid = pthread_getthreadid_np();
        #endif
	}

int main(){
    pthread_id_np_t tid;
    tid = pthread_getthreadid_np();
    foo_pthread();
    bar_pthread();
}

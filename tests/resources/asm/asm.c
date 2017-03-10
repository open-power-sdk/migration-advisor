
#define macro asm("pause");
void main() {
    int test_asm;
    __asm__("mov ax, 1");
    macro
    asm("mov ax, 1");

#if defined __x86_64__
    asm("pause");
#elif defined __powerpc__
    asm("or 27,27,27; isync");
#endif

#define bla
#if defined bla
    __asm__("mov ax, 1");
#endif
}


#define macro asm("pause");
void main() {
    int test_asm;
    __asm__("mov ax, 1");
    macro
    asm("mov ax, 1");

}

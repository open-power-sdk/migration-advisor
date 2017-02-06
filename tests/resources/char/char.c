
#define my_macro char
typedef char my_type;

void safe_chars() {
    // Char Declarations
    char my_char;
    char my_char2;
    signed char my_signed_char;
    unsigned char my_unsigned_char;
    char *my_char_pointer;
    char my_char_array[];
    signed char a = 'D';
    signed char b = 100;
    unsigned char c = 'E';
    unsigned char d = 100;
    char e = 'A';
    const char f = 'B';
    char g = "100";
    char h = my_char;
    char i = my_unsigned_char;
    char j = my_char_pointer;
    char l = my_char_array[0];
    my_macro m = "10";
    my_type n = "10";

    // Char Assignments
    my_signed_char = 10;
    my_signed_char = 'A';
    my_unsigned_char = 20;
    my_unsigned_char = 'B';
    my_char = 'A';
    my_char = "10.0";
    my_char = my_char2;
    my_char = my_unsigned_char;
    my_char = my_char_pointer;
    my_char = my_char_array[0];
}

void problematic_chars() {
    int integer = 10;
    float _float = 10.0
    signed char my_signed_char;
    signed char *my_signed_char_pointer;
    int my_int_array[5];

    // Char Declarations
    char a = 100;
    const char b = 10;
    char c = 10.0;
    char d = integer;
    char e = _float;
    char f = my_signed_char;
    char g = my_signed_char_pointer;
    char h = my_int_array[0];
    my_macro i = 10;
    my_macro j = integer;
    my_type l = 10.0;
    my_type m = integer;

    // Char Assignments
    char my_char;
    my_type my_char2;

    my_char = 100;
    my_char = 10.0;
    my_char = integer;
    my_char = _float;
    my_char = my_signed_char;
    my_char = my_signed_char_pointer;
    my_char = my_int_array[0];
    my_char2 = 100;
    my_char2 = 10.0;
    my_char2 = integer;
    my_char2 = _float;
    my_char2 = my_signed_char;
    my_char2 = my_signed_char_pointer;
    my_char2 = my_int_array[0];
}

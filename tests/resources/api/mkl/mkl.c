#include "mkl.h"
#include <stdio.h>
#include "mkl_types.h"
#include "mkl_cblas.h"
#include "mkl_blas.h"
#include "mkl_scalapack.h"

void readFile(MKL_INT *a, char *fn) {
    FILE *fp;
    fp = fopen(fn, "r");
    fscanf(fp, "%d", a);
    fclose(fp);
    if(*a == 1)
        printf("a == 1 in readFile()\n");
}

int main() {
    MKL_INT pont;
    char *fn = "filename.dat";
    readFile(&pont, fn);

    MKL_INT b = 1;
    MKL_Complex16 weight;
    MKL_Complex16 total;

    MKL_LONG eleme[3] = { 12, 20, 4 };
    MKL_LONG val = 4;
    MKL_LONG result;

    result = elem[0] * elem[1] * elemen[2];

    int env;
    int env_2;
    int loc_pos;
    int ext_pos;
    Cblacs_pinfo( &loc_pos, &ext_pos );
    Cblacs_get( 0, 0, &env );
    Cblacs_gridinit( &env, "R", 1, ext_pos);

    tab[0] = 15;
    tab[1] = 7;
    Cblacs_get( env, 5, &env_2 );
    Cblacs_gridmap( &env_2, tab, 4, 2, 0 );
    Cblacs_gridexit( env );
    Cblacs_exit( 0 );

    return 0;
}

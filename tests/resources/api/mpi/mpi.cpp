#include<mpi.h>

void foo() {
    MPI_Abort();

    MPI_File fh;
    int errorcode;
    MPI_File_call_errhandler(fh, errorcode);

    MPI_Init();

    MPI_Op *op;
    MPI_op_free(op);

    void* buf;
    int count;
    Datatype& datatype;
    MPI::Write_ordered_begin(buf, count, datatype);
    MPI::Init();
}

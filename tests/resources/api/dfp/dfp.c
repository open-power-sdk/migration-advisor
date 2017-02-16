#include <bid_functions.h>

void foo() {
	// tests simple DFP Types
	BID_UINT64 var1, var2, var3;
	var1 = __bid64_maxnum(var2, var3);

	BID_UINT128 y = __bid128_round_integral_negative(y, var1);

	__bid64_round_integral_zero(y, __bid128_fma(var1, var2));

	__bid128_round_integral_negative(var2, var3);
	__bid64_add(var2, var3);
	__bid128_fma(var3, var2);
	__bid64_abs(var1, var2);
	__bid128_copySign(var2, var3);
}

hello:
	addi	$t0, $t0, 3
	j main

bye:
	addi	$t0, $t0, -3
	j	hello
main:
	li	$t0, 4
	bgtz	$t0, hello
	li	$t0, 5
last:
	li	$t1, -2
	j	bye

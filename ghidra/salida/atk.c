// ===== 080159B8 FUN_080159b8

undefined4 FUN_080159b8(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined2 param_4)

{
  uint uVar1;
  undefined4 in_lr;
  
  uVar1 = FUN_0800e6a0(param_1,0,param_2);
  if (uVar1 != 0xff) {
    FUN_08012460(uVar1 & 0xff,param_3,param_4);
  }
  return in_lr;
}


// ===== 080E22EC FUN_080e22ec

void FUN_080e22ec(int param_1)

{
  fast_division(param_1 * 5 + 5,10);
  return;
}


// ===== 0801AB30 (sin funcion)

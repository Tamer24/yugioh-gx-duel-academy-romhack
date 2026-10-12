// ===== 08026A3C FUN_08026a3c

undefined4 FUN_08026a3c(undefined4 param_1,uint param_2,uint param_3,short param_4)

{
  uint uVar1;
  undefined4 in_lr;
  
  uVar1 = -(param_3 & 0xffff) >> 0x1f;
  if (param_4 != 0) {
    uVar1 = uVar1 | 2;
  }
  FUN_08026970(param_1,1,param_2 & 0xff | 0xff00,uVar1);
  return in_lr;
}



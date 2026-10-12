// ===== 08026970 FUN_08026970

undefined4 FUN_08026970(byte param_1,uint param_2,undefined2 param_3,undefined2 param_4)

{
  int iVar1;
  undefined4 in_lr;
  
  iVar1 = DAT_080269b8;
  *(byte *)(DAT_080269b8 + DAT_080269bc) =
       *(byte *)(DAT_080269b8 + DAT_080269bc) & 0xfb | (param_1 & 1) << 2;
  *(uint *)(iVar1 + DAT_080269c0) =
       *(uint *)(iVar1 + DAT_080269c0) & DAT_080269c4 | (param_2 & 0x3f) << 0xc;
  *(undefined2 *)(iVar1 + DAT_080269c8) = param_3;
  *(undefined2 *)(iVar1 + DAT_080269cc) = param_4;
  FUN_080268c0();
  return in_lr;
}



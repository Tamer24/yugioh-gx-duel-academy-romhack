// ===== 08021FE8 drawing_FUN_08021fe8

undefined4
drawing_FUN_08021fe8(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4)

{
  int iVar1;
  byte *pbVar2;
  undefined4 in_lr;
  
  iVar1 = DAT_08022028;
  pbVar2 = (byte *)(DAT_08022028 + DAT_0802202c);
  *(undefined2 *)((uint)*pbVar2 * 8 + DAT_08022028 + 0xc) = param_1;
  *(undefined2 *)((uint)*pbVar2 * 8 + iVar1 + 0xe) = param_2;
  *(undefined2 *)((uint)*pbVar2 * 8 + iVar1 + 0x10) = param_3;
  *(undefined2 *)((uint)*pbVar2 * 8 + iVar1 + 0x12) = param_4;
  *(undefined1 *)((uint)*pbVar2 + iVar1 + DAT_08022030) = 4;
  *pbVar2 = *pbVar2 + 1;
  return in_lr;
}


// ===== 080159E0 FUN_080159e0

undefined8 FUN_080159e0(undefined4 param_1,undefined4 param_2)

{
  undefined4 in_lr;
  undefined1 auStack_10 [4];
  undefined4 local_c;
  undefined4 uStack_4;
  
  uStack_4 = in_lr;
  FUN_080159b8(param_1,param_2,auStack_10,1);
  return CONCAT44(uStack_4,local_c);
}


// ===== 0801A5BC FUN_0801a5bc

undefined4 FUN_0801a5bc(int param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4)

{
  undefined4 uVar1;
  undefined4 in_lr;
  
  uVar1 = 0x4b;
  if (param_1 != 0) {
    uVar1 = DAT_0801a5e0;
  }
  drawing_FUN_08021fe8(uVar1,param_2,param_3,param_4);
  return in_lr;
}



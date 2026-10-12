// ===== 0801C4C8 FUN_0801c4c8

undefined4 FUN_0801c4c8(void)

{
  ushort *puVar1;
  undefined4 in_lr;
  
  puVar1 = DAT_0801c4f0;
  FUN_0800e918(*DAT_0801c4f0 >> 0xf,1,DAT_0801c4f0[1],DAT_0801c4f0[2]);
  *(byte *)(puVar1 + 0x488) = (byte)puVar1[0x488] & 0xdf;
  return in_lr;
}


// ===== 0801C4F4 FUN_0801c4f4

undefined4 FUN_0801c4f4(void)

{
  undefined4 in_lr;
  
  if (DAT_0801c510[3] == 0) {
    FUN_0800eac4(DAT_0801c510[1],*DAT_0801c510 >> 0xf,DAT_0801c510[1],DAT_0801c510[2]);
  }
  else {
    FUN_0800e918(*DAT_0801c510 >> 0xf,2);
  }
  *(byte *)(DAT_0801c530 + 0x910) = *(byte *)(DAT_0801c530 + 0x910) & 0xdf;
  return in_lr;
}


// ===== 0801C534 FUN_0801c534

undefined4 FUN_0801c534(void)

{
  ushort *puVar1;
  undefined4 in_lr;
  
  puVar1 = DAT_0801c55c;
  FUN_0800e918(*DAT_0801c55c >> 0xf,DAT_0801c55c[3],DAT_0801c55c[1],DAT_0801c55c[2]);
  *(byte *)(puVar1 + 0x488) = (byte)puVar1[0x488] & 0xdf;
  return in_lr;
}


// ===== 080617EC FUN_080617ec

undefined4 FUN_080617ec(undefined4 param_1,uint param_2,uint param_3)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  uint uVar4;
  
  iVar1 = FUN_08061730(param_2);
  if (iVar1 != -1) {
    iVar3 = (param_3 & 0x7f) * 0x50 + DAT_080618d8 * ((int)(param_3 & 0x80) >> 7) + DAT_080618dc;
    if (((*(uint *)((param_2 & 0x7f) * 0x50 + DAT_080618d8 * ((int)(param_2 & 0x80) >> 7) +
                    DAT_080618dc + 0x30) & 0xfffff) >> 0xc & 0x80) ==
        ((*(uint *)(iVar3 + 0x30) & 0xfffff) >> 0xc & 0x80)) {
      uVar4 = (uint)*(ushort *)(iVar3 + 0x24);
      iVar1 = iVar1 * 8 + DAT_080618e4;
      if ((*(short *)((uVar4 & 0x7fff) * 2 + SUB_080618e0) == *(short *)(iVar1 + 2)) ||
         (*(short *)((uVar4 & 0x7fff) * 2 + SUB_080618e0) == *(short *)(iVar1 + 4))) {
        iVar1 = (param_3 & 0x7f) * 0x50 + DAT_080618d8 * ((int)(param_3 & 0x80) >> 7) + DAT_080618dc
        ;
        if ((((*(uint *)(iVar1 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0) &&
           ((((int)((uint)*(byte *)(iVar1 + 0x33) * 0x8000000) < 0 &&
             (iVar1 = FUN_0806178c(param_3), iVar1 == 0xff)) &&
            (iVar1 = FUN_08011120(param_1), iVar1 != -1)))) {
          uVar2 = FUN_0800e158(param_2,0x13);
          return uVar2;
        }
      }
    }
  }
  return 0;
}


// ===== 08011120 FUN_08011120

void FUN_08011120(undefined4 param_1)

{
  FUN_080110dc(param_1,0);
  return;
}



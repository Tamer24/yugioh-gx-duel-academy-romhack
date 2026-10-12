// ===== 0801B9F4 FUN_0801b9f4

undefined4 FUN_0801b9f4(void)

{
  int iVar1;
  undefined4 in_lr;
  
  iVar1 = DAT_0801ba24;
  FUN_0800e0e0((*(ushort *)(DAT_0801ba24 + 2) & 0x80) >> 7,*(ushort *)(DAT_0801ba24 + 2) & 0x7f,
               *(undefined2 *)(DAT_0801ba24 + 4));
  *(byte *)(iVar1 + 0x910) = *(byte *)(iVar1 + 0x910) & 0xdf;
  return in_lr;
}


// ===== 0801BA28 FUN_0801ba28

undefined4 FUN_0801ba28(void)

{
  int iVar1;
  undefined4 in_lr;
  
  iVar1 = DAT_0801ba58;
  FUN_0800e11c((*(ushort *)(DAT_0801ba58 + 2) & 0x80) >> 7,*(ushort *)(DAT_0801ba58 + 2) & 0x7f,
               *(undefined2 *)(DAT_0801ba58 + 4));
  *(byte *)(iVar1 + 0x910) = *(byte *)(iVar1 + 0x910) & 0xdf;
  return in_lr;
}


// ===== 0806149C FUN_0806149c

undefined8 FUN_0806149c(ushort *param_1,uint param_2)

{
  undefined4 uVar1;
  int iVar2;
  uint uVar3;
  undefined4 in_lr;
  
  if ((*(uint *)((*(ushort *)
                   (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                    DAT_08061534 * ((*param_1 & 0x1ff) >> 8) + DAT_08061530 + 0x24) & 0x7fff) * 4 +
                DAT_0806152c) & 0x1f00000) == 0x1600000) {
    iVar2 = (param_2 & 0x7f) * 0x50 + DAT_08061534 * ((param_2 & 0x80) >> 7) + DAT_08061530;
    uVar3 = (uint)*(byte *)(iVar2 + 0x33);
    if (((-1 < (int)(uVar3 * 0x8000000)) && ((int)(uVar3 * 0x4000000) < 0)) &&
       (*(ushort *)((*(ushort *)(iVar2 + 0x24) & 0x7fff) * 2 + DAT_08061538) == DAT_0806153c)) {
      uVar1 = 0x3a;
      if ((*param_1 & 1) != 0) {
        uVar1 = DAT_08061570;
      }
      drawing_FUN_08022084(uVar1,param_2 & 0xffff);
      FUN_0801aa84((byte)*param_1 & 1,param_2 & 0xffff);
      uVar1 = 1;
      goto LAB_08061564;
    }
  }
  uVar1 = 0;
LAB_08061564:
  return CONCAT44(in_lr,uVar1);
}


// ===== 08018850 FUN_08018850

undefined8 FUN_08018850(uint param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 in_lr;
  
  iVar1 = FUN_08015c78();
  if (iVar1 == 0) {
    uVar2 = 0;
  }
  else {
    uVar2 = 0x3c;
    if (((*(uint *)((param_1 & 0x7f) * 0x50 + DAT_0801889c * ((int)(param_1 & 0x80) >> 7) +
                    DAT_08018898 + 0x30) & 0xfffff) >> 0xc & 0x80) != 0) {
      uVar2 = DAT_080188a0;
    }
    drawing_FUN_08022034(uVar2,param_1 & 0xffff,0xe);
    uVar2 = 1;
  }
  return CONCAT44(in_lr,uVar2);
}



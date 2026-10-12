// ===== 0806629C FUN_0806629c

undefined8 FUN_0806629c(void)

{
  int iVar1;
  int iVar2;
  undefined1 uVar3;
  undefined4 uVar4;
  int iVar5;
  short *psVar6;
  int iVar7;
  char *pcVar8;
  undefined4 in_lr;
  
  iVar2 = DAT_080662b4;
  pcVar8 = (char *)(DAT_080662b4 + DAT_080662b8);
  if (*pcVar8 == '\0') {
    iVar5 = FUN_0806162c(*(ushort *)
                          (((*(ushort *)(DAT_080662b4 + DAT_08066358) & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_0806635c * ((*(ushort *)(DAT_080662b4 + DAT_08066358) & 0x1ff) >> 8)
                           + DAT_08066354 + 0x24) & 0x7fff);
    iVar1 = DAT_08066360;
    psVar6 = (short *)(DAT_08066360 + 2000);
    *psVar6 = (short)iVar5;
    if ((-1 < iVar5 * 0x10000) &&
       (iVar5 = *(int *)(*psVar6 * 0x1c + DAT_08066368 + 4), *(int *)(iVar1 + DAT_08066364) = iVar5,
       iVar5 != 0)) {
      *(undefined1 *)(iVar1 + DAT_0806636c) = 0x80;
      *(undefined1 *)(iVar1 + DAT_08066370) = 0;
      *pcVar8 = *pcVar8 + '\x01';
      goto LAB_08066330;
    }
  }
  else if (*pcVar8 == '\x01') {
LAB_08066330:
    if ((*(byte *)(iVar2 + 0x5e0) & 1) == 0) {
      uVar4 = *(undefined4 *)(DAT_080663ac + DAT_080663b0);
      iVar7 = 0;
      iVar5 = DAT_080663ac;
      iVar1 = DAT_080663b4;
    }
    else {
      iVar7 = iVar2 + 0x5bc;
      uVar4 = *(undefined4 *)(DAT_08066360 + DAT_08066364);
      iVar5 = DAT_08066360;
      iVar1 = DAT_08066358;
    }
    uVar3 = call_function_bx_r2(iVar2 + iVar1,iVar7,uVar4);
    *(undefined1 *)(iVar5 + DAT_080663b8) = uVar3;
    if (*(char *)(DAT_080663ac + DAT_080663b8) == '\0') {
      *(char *)(DAT_080663bc + SUB_080663c0) = *(char *)(DAT_080663bc + SUB_080663c0) + '\x01';
    }
    uVar4 = 0;
    goto LAB_080663a6;
  }
  uVar4 = 1;
LAB_080663a6:
  return CONCAT44(in_lr,uVar4);
}


// ===== 080195A8 FUN_080195a8

undefined8 FUN_080195a8(undefined4 param_1,undefined4 param_2,undefined2 param_3)

{
  char cVar1;
  uint uVar2;
  undefined4 in_lr;
  
  cVar1 = FUN_0800e6a0(param_1,0xf,param_2);
  if (cVar1 == -1) {
    uVar2 = 0;
  }
  else {
    uVar2 = FUN_08019598(param_1,cVar1,param_3);
    uVar2 = uVar2 & 0xffff;
  }
  return CONCAT44(in_lr,uVar2);
}



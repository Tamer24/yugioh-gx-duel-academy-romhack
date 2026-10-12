// ===== 08066088 FUN_08066088

undefined8 FUN_08066088(void)

{
  int iVar1;
  short sVar2;
  undefined4 uVar3;
  ushort *puVar4;
  short *psVar5;
  int iVar6;
  char *pcVar7;
  undefined4 in_lr;
  
  pcVar7 = (char *)(DAT_080660a0 + DAT_080660a4);
  if (*pcVar7 == '\0') {
    iVar6 = FUN_0806162c(*(ushort *)
                          (((*(ushort *)(DAT_080660a0 + DAT_0806611c) & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_08066120 * ((*(ushort *)(DAT_080660a0 + DAT_0806611c) & 0x1ff) >> 8)
                           + DAT_08066118 + 0x24) & 0x7fff);
    iVar1 = DAT_08066124;
    psVar5 = (short *)(DAT_08066124 + 2000);
    *psVar5 = (short)iVar6;
    if ((-1 < iVar6 * 0x10000) &&
       (iVar6 = *(int *)(*psVar5 * 0x1c + DAT_0806612c + 0x14),
       *(int *)(iVar1 + DAT_08066128) = iVar6, iVar6 != 0)) {
      puVar4 = (ushort *)(iVar1 + 0x7c0);
      *puVar4 = (ushort)DAT_08066130 & *puVar4;
LAB_08066178:
      *pcVar7 = *pcVar7 + '\x01';
      goto LAB_0806617e;
    }
  }
  else if (*pcVar7 == '\x01') {
    if ((*(byte *)(DAT_080660a0 + 0x5e0) & 1) == 0) {
      uVar3 = *(undefined4 *)(DAT_08066188 + DAT_0806618c);
      iVar6 = 0;
      iVar1 = DAT_08066190;
    }
    else {
      iVar6 = DAT_080660a0 + 0x5bc;
      uVar3 = *(undefined4 *)(DAT_08066154 + DAT_08066158);
      iVar1 = DAT_0806615c;
    }
    sVar2 = call_function_bx_r2(DAT_080660a0 + iVar1,iVar6,uVar3);
    if (sVar2 != 0) goto LAB_08066178;
LAB_0806617e:
    uVar3 = 0;
    goto LAB_08066180;
  }
  uVar3 = 1;
LAB_08066180:
  return CONCAT44(in_lr,uVar3);
}


// ===== 08066194 FUN_08066194

undefined8 FUN_08066194(void)

{
  int iVar1;
  short sVar2;
  undefined4 uVar3;
  short *psVar4;
  int iVar5;
  uint *puVar6;
  char *pcVar7;
  undefined4 in_lr;
  
  pcVar7 = (char *)(DAT_080661ac + DAT_080661b0);
  if (*pcVar7 == '\0') {
    iVar5 = FUN_0806162c(*(ushort *)
                          (((*(ushort *)(DAT_080661ac + DAT_08066228) & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_0806622c * ((*(ushort *)(DAT_080661ac + DAT_08066228) & 0x1ff) >> 8)
                           + DAT_08066224 + 0x24) & 0x7fff);
    iVar1 = DAT_08066230;
    psVar4 = (short *)(DAT_08066230 + 2000);
    *psVar4 = (short)iVar5;
    if ((-1 < iVar5 * 0x10000) &&
       (iVar5 = *(int *)(*psVar4 * 0x1c + DAT_08066234 + 0x18), *(int *)(iVar1 + 0x7e0) = iVar5,
       iVar5 != 0)) {
      puVar6 = (uint *)(iVar1 + 0x7c0);
      *puVar6 = *puVar6 & DAT_08066238;
LAB_08066286:
      *pcVar7 = *pcVar7 + '\x01';
      goto LAB_0806628c;
    }
  }
  else if (*pcVar7 == '\x01') {
    if ((*(byte *)(DAT_080661ac + 0x5e0) & 1) == 0) {
      uVar3 = *(undefined4 *)(DAT_08066294 + 0x7e0);
      iVar5 = 0;
      iVar1 = DAT_08066298;
    }
    else {
      iVar5 = DAT_080661ac + SUB_08066268;
      uVar3 = *(undefined4 *)(DAT_08066260 + 0x7e0);
      iVar1 = SUB_08066264;
    }
    sVar2 = call_function_bx_r2(DAT_080661ac + iVar1,iVar5,uVar3);
    if (sVar2 != 0) goto LAB_08066286;
LAB_0806628c:
    uVar3 = 0;
    goto LAB_0806628e;
  }
  uVar3 = 1;
LAB_0806628e:
  return CONCAT44(in_lr,uVar3);
}


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



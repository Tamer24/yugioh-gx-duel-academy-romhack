// ===== 0803451C FUN_0803451c

undefined8 FUN_0803451c(byte *param_1,undefined4 param_2)

{
  uint uVar1;
  int iVar2;
  undefined4 in_lr;
  
  iVar2 = DAT_08034550 * (1 - (*param_1 & 1)) + DAT_0803454c;
  if ((*(byte *)(iVar2 + 0x1c) & 0x3f) == 0 && -1 < *(char *)(iVar2 + 0x1b)) {
    uVar1 = 0;
  }
  else {
    uVar1 = FUN_08032ce4(param_1,param_2);
    uVar1 = uVar1 & 0xffff;
  }
  return CONCAT44(in_lr,uVar1);
}


// ===== 08019598 FUN_08019598

undefined8 FUN_08019598(undefined4 param_1,undefined4 param_2)

{
  undefined4 in_lr;
  
  FUN_08018518(param_1,param_2,0xff);
  return CONCAT44(in_lr,1);
}


// ===== 0807303C FUN_0807303c

undefined8 FUN_0807303c(undefined4 param_1,uint param_2)

{
  byte bVar1;
  short *psVar2;
  undefined4 uVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  uint uVar9;
  undefined4 in_lr;
  
  iVar8 = 0xff;
  iVar7 = 0;
  uVar5 = (uint)(*(byte *)(DAT_080730ec + DAT_080730e8) >> 7);
  uVar9 = DAT_080730e4;
  if ((*(byte *)(DAT_080730f0 + DAT_080730e8) & 0x3f) != 0 || uVar5 != 0) {
    do {
      bVar1 = *(byte *)(iVar7 + DAT_080730f4);
      uVar4 = 0;
      iVar6 = iVar7 + 1;
      psVar2 = DAT_08073100;
      do {
        if (((*(short *)((*(ushort *)
                           ((bVar1 & 0x7f) * 0x50 + (uint)(bVar1 >> 7) * DAT_080730f8 + DAT_080730e8
                           + 0x24) & 0x7fff) * 2 + DAT_080730fc) == *psVar2) && (bVar1 != param_2))
           && ((int)uVar4 < (int)uVar9)) {
          iVar8 = iVar7;
          uVar9 = uVar4;
        }
        psVar2 = psVar2 + 1;
        uVar4 = uVar4 + 1;
      } while (uVar4 < 3);
      iVar7 = iVar6;
    } while (iVar6 < (int)((*(byte *)(DAT_080730f0 + DAT_080730e8) & 0x3f) << 1 | uVar5));
  }
  if (iVar8 != 0xff) {
    uVar9 = (uint)*(byte *)(iVar8 + DAT_08073104 + DAT_080730e8);
    goto LAB_08073198;
  }
  bVar1 = (*(byte *)(DAT_080730e8 + DAT_08073134) & 0x3f) << 1 |
          *(byte *)(DAT_080730e8 + DAT_08073130) >> 7;
  if (bVar1 == 1) {
    uVar9 = (uint)*(byte *)(DAT_080730e8 + DAT_0807314c);
    if (uVar9 != param_2) goto LAB_08073198;
LAB_08073148:
    uVar9 = 0xff;
  }
  else {
    if (bVar1 < 2) {
      if (bVar1 == 0) goto LAB_08073148;
    }
    else if (bVar1 == 2) {
      uVar9 = (uint)*(byte *)(DAT_08073164 + DAT_080730e8);
      if (uVar9 == param_2) {
        uVar9 = (uint)*(byte *)(DAT_08073168 + DAT_080730e8);
      }
      goto LAB_08073198;
    }
    do {
      uVar3 = FUN_080e5740();
      iVar7 = DAT_080731a8;
      iVar8 = fast_modulo2(uVar3,(*(byte *)(DAT_080731a8 + DAT_080731b0) & 0x3f) << 1 |
                                 *(byte *)(DAT_080731a8 + DAT_080731ac) >> 7);
      uVar9 = (uint)*(byte *)(iVar8 + iVar7 + DAT_080731b4);
    } while (uVar9 == param_2);
  }
LAB_08073198:
  return CONCAT44(in_lr,uVar9);
}



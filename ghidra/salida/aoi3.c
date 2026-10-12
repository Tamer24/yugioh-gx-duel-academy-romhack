// ===== 0805CFB0 FUN_0805cfb0

void FUN_0805cfb0(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int unaff_r8;
  undefined4 uStack00000084;
  
  iVar1 = DAT_0805d008;
  uStack00000084 = 0;
  iVar4 = 0;
  iVar3 = DAT_0805d00c * (1 - unaff_r8);
  iVar2 = iVar3 + DAT_0805d008;
  if ((*(byte *)(iVar2 + 0x1c) & 0x3f) != 0 || *(char *)(iVar2 + 0x1b) < '\0') {
    do {
      remove_card_from_effect_register(*(undefined1 *)(iVar4 + iVar3 + iVar1 + DAT_0805d010));
      iVar4 = iVar4 + 1;
    } while (iVar4 < (int)((*(byte *)(iVar2 + 0x1c) & 0x3f) << 1 |
                          (uint)(*(byte *)(iVar2 + 0x1b) >> 7)));
                    /* WARNING: Subroutine does not return */
    FUN_08061382();
  }
                    /* WARNING: Subroutine does not return */
  FUN_08061382();
}


// ===== 08061382 FUN_08061382

void FUN_08061382(void)

{
  short sVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  int iVar8;
  int in_stack_00000080;
  int in_stack_00000084;
  code *UNRECOVERED_JUMPTABLE;
  
  iVar2 = FUN_0800b858();
  if (iVar2 == 0) {
    uVar3 = 0;
  }
  else {
    sVar1 = FUN_08010cac();
    iVar2 = DAT_080613bc;
    if ((sVar1 == 0) && (in_stack_00000080 == 0)) {
      iVar8 = 0;
      while (iVar4 = FUN_0800b858(), iVar8 < iVar4) {
        uVar5 = FUN_0800b86c(iVar8);
        iVar4 = FUN_080dcdc0(*(ushort *)
                              ((uVar5 & 0x7f) * 0x50 + DAT_080613fc * ((int)(uVar5 & 0x80) >> 7) +
                               iVar2 + 0x24) & 0x7fff);
        if ((iVar4 < 3) && (0 < iVar4)) {
          FUN_0800b7fc(uVar5);
        }
        else {
          iVar8 = iVar8 + 1;
        }
      }
    }
    iVar8 = DAT_0806141c;
    iVar2 = DAT_08061418;
    if (in_stack_00000084 != 0) {
      iVar4 = 0;
      while (iVar6 = FUN_0800b858(), iVar4 < iVar6) {
        uVar5 = FUN_0800b86c(iVar4);
        uVar7 = (uint)*(ushort *)
                       ((*(ushort *)
                          ((uVar5 & 0x7f) * 0x50 + DAT_0806145c * ((int)(uVar5 & 0x80) >> 7) + iVar8
                          + 0x24) & 0x7fff) * 2 + iVar2);
        if (uVar7 == DAT_08061460) {
LAB_08061470:
          FUN_0800b7fc(uVar5);
        }
        else {
          if ((int)DAT_08061460 < (int)uVar7) {
            if (((int)uVar7 <= DAT_08061478) && (DAT_08061478 + -1 <= (int)uVar7))
            goto LAB_08061470;
          }
          else if (uVar7 == DAT_08061460 - 3) goto LAB_08061470;
          iVar4 = iVar4 + 1;
        }
      }
    }
    uVar3 = FUN_0800b858();
  }
                    /* WARNING: Could not recover jumptable at 0x08061498. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(uVar3);
  return;
}



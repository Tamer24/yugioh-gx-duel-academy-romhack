// ===== 08042404 FUN_08042404

longlong FUN_08042404(int param_1,undefined4 param_2)

{
  uint uVar1;
  code *UNRECOVERED_JUMPTABLE;
  uint in_lr;
  longlong lVar2;
  
  if (((*(byte *)(param_1 + 2) & 8) == 0) &&
     (uVar1 = *(byte *)(DAT_08042430 + DAT_08042434) - 0x78, uVar1 < 9)) {
    UNRECOVERED_JUMPTABLE = *(code **)(uVar1 * 4 + DAT_08042438);
                    /* WARNING: Could not recover jumptable at 0x0804242e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    lVar2 = (*UNRECOVERED_JUMPTABLE)(UNRECOVERED_JUMPTABLE,DAT_08042438,param_2);
    return lVar2;
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 08033FB0 FUN_08033fb0

undefined8 FUN_08033fb0(ushort *param_1)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  undefined4 in_lr;
  
  iVar7 = 0;
  iVar8 = 0;
  iVar1 = count_empty_field_slots((byte)*param_1 & 1);
  if (iVar1 != 0) {
    iVar5 = 0;
    uVar4 = (uint)(byte)*param_1;
    iVar1 = DAT_08034070 * -((int)(uVar4 << 0x1f) >> 0x1f) + DAT_0803406c;
    if ((*(byte *)(iVar1 + 0x1c) & 0x3f) != 0 || *(char *)(iVar1 + 0x1b) < '\0') {
      iVar6 = DAT_08034074 + DAT_0803406c;
      iVar1 = DAT_08034070;
      iVar9 = DAT_0803406c;
      do {
        iVar3 = (int)(uVar4 << 0x1f) >> 0x1f;
        if ((uint)*(byte *)(iVar5 + iVar1 * -iVar3 + iVar6) != (*param_1 & 0x1ff) >> 1) {
          uVar4 = *(ushort *)
                   ((*(byte *)(iVar5 + iVar1 * -iVar3 + iVar6) & 0x7f) * 0x50 +
                    iVar1 * -((int)((*(byte *)(iVar5 + iVar1 * -iVar3 + iVar6) & 0x80) << 0x18) >>
                             0x1f) + iVar9 + 0x24) & 0x7fff;
          if ((*(uint *)(uVar4 * 4 + DAT_08034078) & 0x1f00000) >> 0x14 < 0x15) {
            iVar1 = FUN_080dd328(uVar4);
            if (iVar1 == 0) {
              iVar8 = iVar8 + 1;
            }
          }
          else {
            iVar7 = iVar7 + 1;
          }
        }
        iVar5 = iVar5 + 1;
        uVar4 = (uint)(byte)*param_1;
        iVar3 = DAT_080340bc * -((int)(uVar4 << 0x1f) >> 0x1f) + DAT_080340b8;
        iVar1 = DAT_080340bc;
        iVar9 = DAT_080340b8;
      } while (iVar5 < (int)((*(byte *)(iVar3 + 0x1c) & 0x3f) << 1 |
                            (uint)(*(byte *)(iVar3 + 0x1b) >> 7)));
    }
    if ((iVar8 != 0) && (1 < iVar7)) {
      uVar2 = 1;
      goto LAB_080340c2;
    }
  }
  uVar2 = 0;
LAB_080340c2:
  return CONCAT44(in_lr,uVar2);
}



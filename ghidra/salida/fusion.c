// ===== 0804FB3C card_type_classifier

undefined8 card_type_classifier(uint param_1)

{
  ushort uVar1;
  ushort uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  undefined4 in_lr;
  
  uVar1 = *(ushort *)
           ((*(ushort *)
              ((param_1 & 0x7f) * 0x50 + ((int)(param_1 & 0x80) >> 7) * DAT_0804fb8c + DAT_0804fb88
              + 0x24) & 0x7fff) * 2 + DAT_0804fb84);
  uVar5 = 0x4f;
  uVar6 = 0;
  while( true ) {
    uVar4 = (uVar6 + uVar5) / 2;
    uVar2 = *(ushort *)(uVar4 * 0x10 + DAT_0804fb90);
    uVar3 = uVar4;
    if (((uVar2 == uVar1) || (uVar3 = uVar6, *(ushort *)(uVar6 * 0x10 + DAT_0804fb90) == uVar1)) ||
       (uVar3 = uVar5, *(ushort *)(uVar5 * 0x10 + DAT_0804fb90) == uVar1)) goto LAB_0804fbd6;
    if (uVar6 == uVar5) break;
    if (uVar2 < uVar1) {
      uVar6 = uVar4;
    }
    if (uVar1 < uVar2) {
      uVar5 = uVar4;
    }
    if ((uVar6 + uVar5) / 2 == uVar4) {
      uVar6 = uVar5;
    }
  }
  uVar3 = 0xffffffff;
LAB_0804fbd6:
  return CONCAT44(in_lr,uVar3);
}


// ===== 0804FDD8 validate_target_list

undefined8 validate_target_list(uint param_1,uint param_2,int param_3,int param_4,short param_5)

{
  bool bVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  uint uVar8;
  int iVar9;
  undefined4 in_lr;
  
  iVar9 = 0;
  iVar2 = card_type_classifier(param_2 & 0xff);
  iVar3 = count_empty_field_slots(param_1);
  bVar1 = 0 < iVar3;
  if ((0x1a < ((param_2 & 0x7f) - 100 & 0xff)) && (-1 < iVar2)) {
    iVar2 = iVar2 * 0x10;
    uVar8 = 0;
    if ((*(byte *)(iVar2 + DAT_0804fe88 + 2) & 7) == 2) {
      uVar8 = 4;
    }
    iVar3 = 0;
    if (0 < param_4) {
      do {
        uVar6 = (uint)*(byte *)(param_3 + iVar3);
        uVar5 = (*(uint *)((uVar6 & 0x7f) * 0x50 + DAT_0804fe8c * ((int)(uVar6 & 0x80) >> 7) +
                           DAT_0804fe90 + 0x30) & 0xfffff) >> 0xc & 0x7f;
        if (uVar5 != 0xd) {
          if (uVar5 < 0xe) {
            if (uVar5 != 0) goto LAB_0804ff06;
          }
          else if (uVar5 != 0xf) goto LAB_0804ff06;
        }
        iVar7 = (uVar6 & 0x7f) * 0x50 + DAT_0804ff0c * ((int)(uVar6 & 0x80) >> 7) + DAT_0804ff10;
        if ((*(uint *)(iVar7 + 0x30) & 0xfffff) >> 0x13 != param_1) goto LAB_0804ff06;
        uVar5 = targeting_mode_filter(uVar6,param_2 & 0xff,uVar8);
        if ((int)uVar5 < 1) {
          if (param_5 != 0) goto LAB_0804ff06;
        }
        else {
          uVar8 = uVar8 | uVar5;
          iVar9 = iVar9 + 1;
          if (((*(uint *)(iVar7 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0) {
            bVar1 = true;
          }
          if ((param_5 != 0) && ((int)(*(byte *)(iVar2 + DAT_0804ff14 + 2) & 7) < iVar9))
          goto LAB_0804ff06;
        }
        iVar3 = iVar3 + 1;
      } while (iVar3 < param_4);
    }
    if (*(ushort *)
         ((*(ushort *)
            ((param_2 & 0x7f) * 0x50 + DAT_0804ff68 * -((int)((param_2 & 0x80) << 0x18) >> 0x1f) +
             DAT_0804ff64 + 0x24) & 0x7fff) * 2 + DAT_0804ff60) == DAT_0804ff6c) {
      if (4 < iVar9) {
LAB_0804ff74:
        if (bVar1) {
          if (param_5 == 0) {
            uVar8 = *(byte *)(iVar2 + DAT_0804ffbc + 2) & 7;
          }
          else {
            uVar8 = *(byte *)(iVar2 + DAT_0804ff94 + 2) & 7;
            if ((int)uVar8 < iVar9) goto LAB_0804ff06;
          }
          if ((int)uVar8 <= iVar9) {
            uVar4 = 1;
            goto LAB_0804ffaa;
          }
        }
      }
    }
    else if (uVar8 == 7) goto LAB_0804ff74;
  }
LAB_0804ff06:
  uVar4 = 0;
LAB_0804ffaa:
  return CONCAT44(in_lr,uVar4);
}


// ===== 080502FC effect_dispatch_execute

longlong effect_dispatch_execute(int param_1,undefined4 param_2)

{
  int iVar1;
  uint uVar2;
  uint in_lr;
  longlong lVar3;
  
  if ((((*(byte *)(param_1 + 2) & 8) == 0) &&
      (iVar1 = effect_activation_gatekeeper(param_1,param_2), iVar1 != 0)) &&
     (uVar2 = *(byte *)(DAT_08050340 + DAT_08050344) - 0x62, uVar2 < 0x1f)) {
                    /* WARNING: Could not recover jumptable at 0x0805033e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    lVar3 = (**(code **)(uVar2 * 4 + DAT_08050348))();
    return lVar3;
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 08050BEC effect_dispatch_condition

longlong effect_dispatch_condition(int param_1,undefined4 param_2)

{
  uint uVar1;
  code *UNRECOVERED_JUMPTABLE;
  uint in_lr;
  longlong lVar2;
  
  if (((*(byte *)(param_1 + 2) & 8) == 0) &&
     (uVar1 = *(byte *)(DAT_08050c20 + DAT_08050c24) - 0x62, uVar1 < 0x1f)) {
    UNRECOVERED_JUMPTABLE = *(code **)(uVar1 * 4 + DAT_08050c28);
                    /* WARNING: Could not recover jumptable at 0x08050c1e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    lVar2 = (*UNRECOVERED_JUMPTABLE)(UNRECOVERED_JUMPTABLE,DAT_08050c28,param_2);
    return lVar2;
  }
  return (ulonglong)in_lr << 0x20;
}



// ===== 0803FA8C FUN_0803fa8c

undefined8 FUN_0803fa8c(ushort *param_1)

{
  byte bVar1;
  ushort uVar2;
  bool bVar3;
  int iVar4;
  undefined4 uVar5;
  uint uVar6;
  int iVar7;
  byte *pbVar8;
  char *pcVar9;
  uint uVar10;
  int iVar11;
  uint uVar12;
  ushort *puVar13;
  int iVar14;
  undefined4 in_lr;
  undefined8 uVar15;
  
  iVar14 = 0x2b08;
  iVar11 = 0x201fd00;
  if ((param_1[1] & 8) == 0) {
    bVar1 = *(byte *)(0x201fd00 + 0x7c6);
    if (bVar1 == 0x7f) {
      iVar7 = 0;
      if ((*(ushort *)
            (0x2b08 * (uint)*(byte *)(0x201fd00 + 0x7c7) + 0x2022250 + 0x1c) &
          0x1fff) >> 6 != 0) {
        do {
          bVar1 = *(byte *)(iVar7 + (uint)*(byte *)(iVar11 + 0x7c7) * iVar14 +
                           0x2022250 + 0x28a4);
          uVar12 = (uint)bVar1;
          uVar10 = *(ushort *)
                    ((uVar12 & 0x7f) * 0x50 + (uint)(bVar1 >> 7) * iVar14 + 0x2022250 + 0x24) &
                   0x7fff;
          bVar3 = true;
          FUN_0801ab04((uint)*(byte *)(iVar11 + 0x7c7),uVar12);
          uVar6 = *(uint *)(uVar10 * 4 + 0x8f243cc);
          if (((((uVar6 & 0x1f00000) >> 0x14 < 0x15) && ((uVar6 & 0x1e000000) >> 0x19 < 5)) &&
              (iVar4 = FUN_080dce18(uVar10), iVar4 == 0)) &&
             ((iVar4 = FUN_080dd328(uVar10), iVar4 == 0 &&
              (iVar4 = FUN_0806dcc0((byte)*param_1 & 1,uVar12), iVar4 != 0)))) {
            uVar2 = *(ushort *)(iVar11 + 0x920);
            *(ushort *)(iVar11 + 0x920) = uVar2 + 1;
            *(byte *)((uint)uVar2 + 0x2020622) = bVar1;
            bVar3 = false;
          }
          if (bVar3) {
            FUN_08018570((byte)*param_1 & 1,uVar12,(*param_1 & 0x1ff) >> 1);
            *0x20204c8 = *0x20204c8 + '\x01';
          }
          iVar7 = iVar7 + 1;
        } while ((iVar7 < 5) &&
                (iVar7 < (int)((*(ushort *)
                                 (0x2b08 * (uint)*(byte *)(iVar11 + 0x7c7) +
                                  0x2022250 + 0x1c) & 0x1fff) >> 6)));
      }
LAB_0803fcba:
      uVar5 = 0x7e;
      goto LAB_0803fd22;
    }
    if (bVar1 < 0x80) {
      if (bVar1 == 0x7e) {
        puVar13 = (ushort *)(0x201fd00 + 0x920);
        if (*puVar13 == 0) {
          pbVar8 = (byte *)(0x201fd00 + 0x7c7);
          *pbVar8 = 1 - *pbVar8;
          iVar14 = 0x2022250;
          iVar7 = 0x2b08 * (uint)*pbVar8 + 0x2022250;
          *(byte *)(iVar11 + 0x7c8) =
               (*(byte *)(iVar7 + 0x1c) & 0x3f) << 1 | *(byte *)(iVar7 + 0x1b) >> 7;
          *puVar13 = 0;
          if ((uint)*pbVar8 == (*(byte *)(iVar14 + 0x562e) & 3) >> 1) {
            uVar5 = 0x78;
          }
          else {
            uVar5 = 0x7f;
          }
          goto LAB_0803fd22;
        }
        *puVar13 = *puVar13 - 1;
        record_monster_set(*(undefined1 *)(iVar11 + 0x7c7),
                           *(undefined1 *)((uint)*puVar13 + iVar11 + 0x922),0,0);
        goto LAB_0803fcba;
      }
    }
    else if (bVar1 == 0x80) {
      cleanup_card_actions();
      iVar11 = 0;
      do {
        iVar14 = iVar11 + 1;
        pcVar9 = (char *)(iVar11 * 0xb + 0x5610 + 0x2022250);
        iVar11 = 4;
        do {
          if (*pcVar9 != -1) {
            uVar15 = send_card_to_graveyard
                               (*pcVar9,((byte)*param_1 & 1) << 0xf | 0x41,(*param_1 & 0x1ff) >> 1);
            return uVar15;
          }
          pcVar9 = pcVar9 + 1;
          iVar11 = iVar11 + -1;
        } while (-1 < iVar11);
        iVar11 = iVar14;
      } while (iVar14 < 2);
      process_card_actions();
      iVar14 = 0x201fd00;
      iVar11 = 0x2022250;
      pbVar8 = (byte *)(0x201fd00 + 0x7c7);
      *pbVar8 = (byte)((*(byte *)(0x2022250 + 0x562e) & 3) >> 1);
      iVar11 = 0x2b08 * (uint)*pbVar8 + iVar11;
      *(byte *)(iVar14 + 0x7c8) =
           (*(byte *)(iVar11 + 0x1c) & 0x3f) << 1 | *(byte *)(iVar11 + 0x1b) >> 7;
      *(undefined2 *)(iVar14 + 0x920) = 0;
      uVar5 = 0x7f;
      goto LAB_0803fd22;
    }
  }
  uVar5 = 0;
LAB_0803fd22:
  return CONCAT44(in_lr,uVar5);
}


// ===== 0803FD30 FUN_0803fd30

longlong FUN_0803fd30(int param_1,undefined4 param_2)

{
  uint uVar1;
  code *UNRECOVERED_JUMPTABLE;
  uint in_lr;
  longlong lVar2;
  
  if (((*(byte *)(param_1 + 2) & 8) == 0) &&
     (uVar1 = *(byte *)(0x201fd00 + 0x7c6) - 0x7c, uVar1 < 5)) {
    UNRECOVERED_JUMPTABLE = *(code **)(uVar1 * 4 + 0x803fd70);
                    /* WARNING: Could not recover jumptable at 0x0803fd62. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    lVar2 = (*UNRECOVERED_JUMPTABLE)(UNRECOVERED_JUMPTABLE,0x803fd70,param_2);
    return lVar2;
  }
  return (ulonglong)in_lr << 0x20;
}



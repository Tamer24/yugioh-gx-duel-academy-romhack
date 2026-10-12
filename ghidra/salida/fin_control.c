// ===== 08065BF8 FUN_08065bf8

undefined8 FUN_08065bf8(void)

{
  byte bVar1;
  bool bVar2;
  ushort uVar3;
  uint uVar4;
  int iVar5;
  undefined4 uVar6;
  int iVar7;
  byte *pbVar8;
  ushort uVar9;
  byte *pbVar10;
  int iVar11;
  undefined4 in_lr;
  undefined8 uVar12;
  
  pbVar8 = DAT_08065f10;
  iVar11 = DAT_08065c50;
  iVar5 = DAT_08065c44;
  pbVar10 = (byte *)(DAT_08065c44 + DAT_08065c48);
  bVar1 = *pbVar10;
  uVar4 = (*(uint *)(DAT_08065c44 + DAT_08065c4c) & 0x7fffff) >> 0xf;
  if (uVar4 == 0) {
    cleanup_card_actions();
    iVar5 = 0;
    do {
      iVar7 = 0;
      iVar11 = iVar5 + 1;
      do {
        bVar2 = false;
        bVar1 = *(byte *)(iVar5 * 0xb + iVar7 + DAT_08065d54 + DAT_08065d58);
        uVar4 = (uint)bVar1;
        if (uVar4 != 0xff) {
          iVar5 = (uVar4 & 0x7f) * 0x50 + (uint)(bVar1 >> 7) * SUB_08065d5c + DAT_08065d54;
          pbVar10 = (byte *)(iVar5 + 0x33);
          pbVar8 = (byte *)(iVar5 + 0x34);
          uVar9 = (ushort)*pbVar8;
          uVar3 = (uVar9 & 3) << 2 | (ushort)(*pbVar10 >> 6);
          if ((uVar3 != 0) &&
             (drawing_FUN_08022034(0x51,uVar4,uVar3 - 1,uVar9,0),
             (byte)((*pbVar8 & 3) << 2 | *pbVar10 >> 6) == 1)) {
            bVar2 = true;
          }
          iVar5 = FUN_0801231c(uVar4,DAT_08065d60,1,0x10);
          if (iVar5 != 0) {
            bVar2 = true;
          }
          iVar5 = FUN_0801231c(uVar4,DAT_08065d64,1,0x10);
          if (iVar5 != 0) {
            bVar2 = true;
          }
          iVar5 = FUN_0801231c(uVar4,DAT_08065d68,1,0x10);
          if (iVar5 != 0) {
            bVar2 = true;
          }
          if (!bVar2) {
            uVar12 = FUN_0800e158(uVar4,0x15);
            return uVar12;
          }
          uVar12 = send_card_to_graveyard(uVar4,0x41,0xff);
          return uVar12;
        }
        iVar7 = iVar7 + 1;
      } while (iVar7 < 5);
      iVar5 = iVar11;
    } while (iVar11 < 2);
    process_card_actions();
  }
  else {
    if (uVar4 != 1) {
      if ((*(byte *)(DAT_08065c50 + 0x208) & 8) == 0) {
        if ((bVar1 & 2) == 0) {
          *DAT_08065f10 = bVar1 & 2;
          pbVar8[1] = bVar1 & 2;
        }
        if ((*(byte *)(iVar11 + 0x208) & 8) != 0) goto LAB_08065eea;
      }
      else {
LAB_08065eea:
        FUN_08026e2c(DAT_08065f14);
      }
      *(short *)(DAT_08065f18 + DAT_08065f1c) = *(short *)(DAT_08065f18 + DAT_08065f1c) + 1;
      uVar6 = 1;
      goto LAB_08065efe;
    }
    uVar6 = 0xd;
    if ((bVar1 & 2) != 0) {
      uVar6 = DAT_08065eb4;
    }
    drawing_FUN_080220d4(uVar6);
    uVar6 = 0xe;
    if ((*pbVar10 & 2) != 0) {
      uVar6 = DAT_08065eb8;
    }
    drawing_FUN_080220d4(uVar6);
    iVar11 = 0;
    do {
      iVar7 = DAT_08065ebc * iVar11 + iVar5;
      pbVar8 = (byte *)(iVar7 + DAT_08065ec0);
      if ((int)((uint)*pbVar8 * 0x40000000) < 0) {
        drawing_FUN_08022084(0x13,((*pbVar8 & 1) << 4 | *(byte *)(iVar7 + DAT_08065ec4) >> 4) + 1);
      }
      iVar11 = iVar11 + 1;
    } while (iVar11 < 2);
  }
  uVar4 = *(uint *)(DAT_08065ec8 + DAT_08065ecc);
  *(uint *)(DAT_08065ec8 + DAT_08065ecc) =
       DAT_08065ed0 & uVar4 | (((uVar4 & 0x7fffff) >> 0xf) + 1 & 0xff) << 0xf;
  uVar6 = 0;
LAB_08065efe:
  return CONCAT44(in_lr,uVar6);
}



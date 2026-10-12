// ===== 0804587C FUN_0804587c

undefined8 FUN_0804587c(ushort *param_1)

{
  byte bVar1;
  bool bVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  byte *pbVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  undefined4 in_lr;
  
  bVar2 = false;
  if ((param_1[1] & 8) == 0) {
    if (*(char *)(0x201fd00 + 0x7c6) == -0x80) {
      iVar9 = 0;
      do {
        if (iVar9 == 0) {
          uVar6 = (byte)*param_1 & 1;
        }
        else {
          uVar6 = 1 - ((byte)*param_1 & 1);
        }
        iVar9 = iVar9 + 1;
        pbVar7 = (byte *)(uVar6 * 0xb + 0x2027860);
        iVar10 = 10;
        do {
          uVar5 = (uint)*pbVar7;
          if ((uVar5 != 0xff) &&
             (FUN_080188ac(uVar5,(uint)(*pbVar7 >> 7) << 0xf | 0x3008),
             uVar5 == (*param_1 & 0x1ff) >> 1)) {
            bVar2 = true;
          }
          iVar4 = 0x2022250;
          pbVar7 = pbVar7 + 1;
          iVar10 = iVar10 + -1;
        } while (-1 < iVar10);
        iVar11 = 0;
        iVar10 = 0x2b08 * uVar6;
        if ((*(byte *)(iVar10 + 0x2022250 + 0x1c) & 0x3f) != 0 ||
            *(char *)(iVar10 + 0x2022250 + 0x1b) < '\0') {
          iVar8 = iVar10 + 0x2022250;
          do {
            bVar1 = *(byte *)(iVar11 + iVar10 + 0x2824 + iVar4);
            FUN_080188ac((uint)bVar1,(uint)(bVar1 >> 7) << 0xf | 0x3008);
            if ((uint)bVar1 == (*param_1 & 0x1ff) >> 1) {
              bVar2 = true;
            }
            iVar11 = iVar11 + 1;
          } while (iVar11 < (int)((*(byte *)(iVar8 + 0x1c) & 0x3f) << 1 |
                                 (uint)(*(byte *)(iVar8 + 0x1b) >> 7)));
        }
        iVar10 = 0x2022250;
        iVar8 = 0;
        iVar11 = 0x2b08 * uVar6;
        if ((*(uint *)(iVar11 + iVar4 + 0x1c) & 0xfffff) >> 0xd != 0) {
          iVar4 = iVar11 + 0x2022250;
          do {
            bVar1 = *(byte *)(iVar8 + iVar11 + iVar10 + 0x2924);
            FUN_080188ac((uint)bVar1,(uint)(bVar1 >> 7) << 0xf | 0x3008);
            if ((uint)bVar1 == (*param_1 & 0x1ff) >> 1) {
              bVar2 = true;
            }
            iVar8 = iVar8 + 1;
          } while (iVar8 < (int)((*(uint *)(iVar4 + 0x1c) & 0xfffff) >> 0xd));
        }
      } while (iVar9 < 2);
      if (!bVar2) {
        FUN_080188ac((*param_1 & 0x1ff) >> 1,0x3008);
      }
      uVar3 = 0x7f;
      goto LAB_08045a3c;
    }
    iVar9 = 0;
    do {
      if (iVar9 == 0) {
        uVar6 = (byte)*param_1 & 1;
      }
      else {
        uVar6 = 1 - ((byte)*param_1 & 1);
      }
      uVar3 = 0x24;
      if (uVar6 != 0) {
        uVar3 = 0x8024;
      }
      drawing_FUN_080220d4(uVar3);
      FUN_0801b28c(uVar6,5);
      iVar9 = iVar9 + 1;
    } while (iVar9 < 2);
  }
  uVar3 = 0;
LAB_08045a3c:
  return CONCAT44(in_lr,uVar3);
}


// ===== 08043904 FUN_08043904

undefined8 FUN_08043904(byte *param_1)

{
  byte bVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 in_lr;
  undefined8 uVar4;
  
  bVar1 = *(byte *)(0x201fd00 + 0x7c6);
  if (bVar1 == 0x7f) {
    fusion_summon_dialogue(*param_1 & 1,0x12,5202/*Fairy Guardian*/,0);
    uVar3 = 0x7e;
  }
  else {
    if (bVar1 < 0x80) {
      if (bVar1 == 0x7e) {
        uVar3 = 0x78;
        goto LAB_0804396e;
      }
    }
    else if ((bVar1 == 0x80) && (iVar2 = FUN_0805aeb0(*param_1 & 1,5202/*Fairy Guardian*/,0), iVar2 != 0)) {
      uVar4 = ask_question(0x9468b40);
      return uVar4;
    }
    uVar3 = 0;
  }
LAB_0804396e:
  return CONCAT44(in_lr,uVar3);
}


// ===== 080430AC FUN_080430ac

undefined8 FUN_080430ac(ushort *param_1)

{
  byte bVar1;
  int iVar2;
  uint uVar3;
  undefined4 uVar4;
  uint uVar5;
  uint uVar6;
  undefined4 in_lr;
  undefined8 uVar7;
  
  uVar5 = 5109/*Return of the Doomed*/;
  bVar1 = *(byte *)(0x201fd00 + 0x7c6);
  if (bVar1 == 0x7f) {
    fusion_summon_dialogue((byte)*param_1 & 1,0x12,5109/*Return of the Doomed*/,0);
    uVar4 = 0x7e;
  }
  else {
    if (bVar1 < 0x80) {
      if (bVar1 == 0x7e) {
        cleanup_card_actions();
        uVar6 = (uint)*param_1;
        uVar5 = (uint)*(ushort *)
                       ((*(ushort *)
                          (((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           0x2b08 * ((uVar6 & 0x1ff) >> 8) + 0x2022250 + 0x24) & 0x7fff) *
                        2 + 0x87a8624);
        if (uVar5 == 5193/*Lady Panther*/) {
          uVar5 = (*(uint *)(0x2019f00 + 0x24) & 0x7ffff) >> 0xb;
          uVar6 = (uVar6 & 0x1ff) >> 1;
          uVar4 = 0x10;
LAB_0804321c:
          uVar7 = send_card_to_graveyard(uVar5,uVar4,uVar6);
          return uVar7;
        }
        if ((int)5193/*Lady Panther*/ < (int)uVar5) {
          if (uVar5 == 5196/*Crimson Sentry*/) {
            uVar5 = (*(uint *)(0x2019f00 + 0x24) & 0x7ffff) >> 0xb;
            uVar6 = (uVar6 & 0x1ff) >> 1;
            uVar4 = 0x20;
            goto LAB_0804321c;
          }
          uVar3 = 5196/*Crimson Sentry*/ + 0xb;
        }
        else {
          uVar3 = 5193/*Lady Panther*/ - 0x54;
        }
        if (uVar5 == uVar3) {
          uVar5 = (*(uint *)(0x2019f00 + 0x24) & 0x7ffff) >> 0xb;
          uVar6 = (uVar6 & 0x1ff) >> 1;
          uVar4 = 4;
          goto LAB_0804321c;
        }
      }
    }
    else if ((bVar1 == 0x80) &&
            (iVar2 = FUN_0805aeb0((byte)*param_1 & 1,5109/*Return of the Doomed*/,0), iVar2 != 0)) {
      uVar6 = (uint)*(ushort *)
                     ((*(ushort *)
                        (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         ((*param_1 & 0x1ff) >> 8) * 0x2b08 + 0x2022250 + 0x24) & 0x7fff) *
                      2 + 0x87a8624);
      uVar4 = 0x9468b1a;
      if (uVar6 == 5193/*Lady Panther*/) {
LAB_0804315a:
        uVar7 = ask_question(uVar4);
        return uVar7;
      }
      if ((int)5193/*Lady Panther*/ < (int)uVar6) {
        if (uVar6 == 5196/*Crimson Sentry*/) goto LAB_0804315a;
        uVar5 = 5196/*Crimson Sentry*/ + 0xb;
      }
      uVar4 = 0x9469136;
      if (uVar6 == uVar5) goto LAB_0804315a;
    }
    uVar4 = 0;
  }
  return CONCAT44(in_lr,uVar4);
}


// ===== 080344B0 FUN_080344b0

undefined8 FUN_080344b0(ushort *param_1)

{
  short sVar1;
  uint uVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 in_lr;
  
  uVar2 = (*param_1 & 0x1ff) >> 1;
  sVar1 = FUN_08010814(uVar2,3,uVar2);
  if ((sVar1 == 0) || (iVar3 = FUN_0805aeb0((byte)*param_1 & 1,5202/*Fairy Guardian*/,0), iVar3 < 1)) {
    uVar4 = 0;
  }
  else {
    uVar4 = 1;
  }
  return CONCAT44(in_lr,uVar4);
}



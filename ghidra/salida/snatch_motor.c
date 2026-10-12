// ===== 0802F9C4 FUN_0802f9c4

undefined8 FUN_0802f9c4(void)

{
  byte bVar1;
  byte bVar2;
  undefined1 uVar3;
  ushort uVar4;
  undefined4 uVar5;
  int iVar6;
  uint uVar7;
  byte *pbVar8;
  ushort *puVar9;
  char *pcVar10;
  uint uVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  undefined4 in_lr;
  undefined8 uVar15;
  byte abStack_9c [24];
  ushort auStack_84 [24];
  undefined1 auStack_54 [4];
  int local_50;
  int iStack_4c;
  uint local_48;
  int local_44;
  int local_40;
  int local_3c;
  uint local_38;
  int iStack_34;
  undefined1 *local_30;
  undefined4 local_2c;
  int local_28;
  undefined4 local_24;
  
  local_50 = 0;
  local_48 = 0;
  local_44 = 0;
  local_40 = 0;
  local_3c = 0;
  local_38 = 0xffffffff;
  if ((((*(byte *)(DAT_0802fab4 + 0x208) & 8) == 0) ||
      ((*(byte *)(DAT_0802fab8 + DAT_0802fabc) & 2) == 0)) &&
     (((*(byte *)(DAT_0802fac0 + DAT_0802fac4) & 0xfe) == 0 ||
      (9 < *(byte *)(DAT_0802fac0 + DAT_0802fac4) >> 1)))) {
    local_30 = auStack_54;
    iVar14 = 0;
    do {
      iVar13 = 0;
      iVar6 = iVar14 + 1;
      pbVar8 = abStack_9c + local_50;
      do {
        bVar1 = *(byte *)(iVar14 * 0xb + iVar13 + DAT_0802fab8 + DAT_0802fac8);
        uVar11 = (uint)bVar1;
        if ((uVar11 != 0xff) && (0x1a < (uVar11 & 0x7f) - 100)) {
          local_24 = 0x80;
          iVar12 = (uVar11 & 0x7f) * 0x50 + DAT_0802facc * (uint)(bVar1 >> 7) + DAT_0802fab8;
          if ((int)((uint)*(byte *)(iVar12 + 0x33) * 0x8000000) < 0) {
            uVar7 = (uint)*(ushort *)((*(ushort *)(iVar12 + 0x24) & 0x7fff) * 2 + DAT_0802fad0);
            if (uVar7 == 0x1360) {
LAB_0802fb58:
              uVar15 = FUN_0800e158(uVar11,0x20);
              return uVar15;
            }
            if (uVar7 < 0x1361) {
              if (uVar7 == 0x1296) {
                if (((*(uint *)(iVar12 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0) {
                  local_40 = 1;
                  *pbVar8 = bVar1;
                  pbVar8 = pbVar8 + 1;
                  local_50 = local_50 + 1;
                }
              }
              else if (uVar7 == 0x1302) {
                local_2c = 0x7f;
                local_28 = DAT_0802facc;
                uVar15 = FUN_0800e158(uVar11,0x20);
                return uVar15;
              }
            }
            else {
              if (uVar7 == DAT_0802fae4) goto LAB_0802fb58;
              if ((uVar7 == DAT_0802fae8) &&
                 (((*(uint *)(iVar12 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0)) {
                *pbVar8 = bVar1;
                pbVar8 = pbVar8 + 1;
                local_50 = local_50 + 1;
              }
            }
          }
        }
        iVar13 = iVar13 + 1;
      } while (iVar13 < 10);
      iVar14 = iVar6;
    } while (iVar6 < 2);
    iStack_34 = local_50 + -1;
    do {
      iStack_4c = 0;
      iVar14 = 0;
      if (0 < iStack_34) {
        do {
          pbVar8 = abStack_9c + iVar14;
          iVar6 = iVar14 + 1;
          bVar1 = abStack_9c[iVar14 + 1];
          if (*(ushort *)
               ((bVar1 & 0x7f) * 0x50 + DAT_0802fc94 * -((int)((bVar1 & 0x80) << 0x18) >> 0x1f) +
                DAT_0802fc90 + 0x26) <
              *(ushort *)
               ((*pbVar8 & 0x7f) * 0x50 + DAT_0802fc94 * -((int)((*pbVar8 & 0x80) << 0x18) >> 0x1f)
                + DAT_0802fc90 + 0x26)) {
            bVar2 = *pbVar8;
            *pbVar8 = bVar1;
            abStack_9c[iVar14 + 1] = bVar2;
            iStack_4c = 1;
          }
          iVar14 = iVar6;
        } while (iVar6 < iStack_34);
      }
    } while (iStack_4c != 0);
    if (local_40 == 0) {
      if ((local_3c != 0) && (iVar14 = 0, 0 < local_50)) {
        do {
          pbVar8 = abStack_9c + iVar14;
          if (((undefined1 *)
               (*(uint *)((*(ushort *)
                            ((*pbVar8 & 0x7f) * 0x50 +
                             DAT_0802fd24 * -((int)((*pbVar8 & 0x80) << 0x18) >> 0x1f) +
                             DAT_0802fd20 + 0x24) & 0x7fff) * 4 + DAT_0802fd1c) & 0x1f00000) ==
               &DAT_01500000) && (local_38 != *pbVar8)) {
            iVar13 = local_50 + -1;
            iVar6 = iVar14;
            if (iVar14 < local_50) {
              do {
                *pbVar8 = pbVar8[1];
                pbVar8 = pbVar8 + 1;
                iVar6 = iVar6 + 1;
              } while (iVar6 < local_50);
            }
            local_50 = iVar13;
          }
          else {
            iVar14 = iVar14 + 1;
          }
        } while (iVar14 < local_50);
      }
    }
    else {
      iVar14 = 0;
      if (0 < local_50) {
        do {
          pbVar8 = abStack_9c + iVar14;
          if ((undefined1 *)
              (*(uint *)((*(ushort *)
                           ((*pbVar8 & 0x7f) * 0x50 +
                            DAT_0802fc94 * -((int)((*pbVar8 & 0x80) << 0x18) >> 0x1f) + DAT_0802fc90
                           + 0x24) & 0x7fff) * 4 + DAT_0802fc98) & 0x1f00000) == &DAT_01500000) {
            iVar13 = local_50 + -1;
            iVar6 = iVar14;
            if (iVar14 < local_50) {
              do {
                *pbVar8 = pbVar8[1];
                pbVar8 = pbVar8 + 1;
                iVar6 = iVar6 + 1;
              } while (iVar6 < local_50);
            }
            local_50 = iVar13;
          }
          else {
            iVar14 = iVar14 + 1;
          }
        } while (iVar14 < local_50);
      }
    }
    iVar14 = 0;
    if (0 < local_50) {
      do {
        uVar11 = (uint)*(ushort *)
                        ((*(ushort *)
                           ((abStack_9c[iVar14] & 0x7f) * 0x50 +
                            DAT_0802fd8c * -((int)((abStack_9c[iVar14] & 0x80) << 0x18) >> 0x1f) +
                            DAT_0802fd88 + 0x24) & 0x7fff) * 2 + DAT_0802fd84);
        if (uVar11 == 0x1360) {
LAB_0802fdb6:
          local_48 = local_48 | 1;
        }
        else if (uVar11 < 0x1361) {
          if ((uVar11 == DAT_0802fd90) || (uVar11 == DAT_0802fd90 + 0x6c)) {
            local_48 = local_48 | 2;
          }
        }
        else if (uVar11 == DAT_0802fda4) {
          local_48 = local_48 & 0xffff | 4;
        }
        else if (uVar11 == DAT_0802fda8) goto LAB_0802fdb6;
        iVar14 = iVar14 + 1;
      } while (iVar14 < local_50);
    }
    iVar14 = 0;
    do {
      iVar6 = 0;
      do {
        bVar1 = *(byte *)(iVar14 * 0xb + iVar6 + DAT_0802feac + DAT_0802feb0);
        uVar11 = (uint)bVar1;
        if (((uVar11 != 0xff) && (0x1a < (uVar11 & 0x7f) - 100)) &&
           ((int)((uint)*(byte *)((uVar11 & 0x7f) * 0x50 + (uint)(bVar1 >> 7) * DAT_0802feb4 +
                                  DAT_0802feac + 0x33) * 0x8000000) < 0)) {
          uVar15 = FUN_0800e158(uVar11,0x1f);
          return uVar15;
        }
        iVar6 = iVar6 + 1;
      } while (iVar6 < 0xb);
      iVar14 = iVar14 + 1;
    } while (iVar14 < 2);
    iVar6 = DAT_08030064 + DAT_08030068;
    iVar14 = 0;
    do {
      puVar9 = (ushort *)(local_30 + iVar14 * 2);
      *puVar9 = 0;
      uVar11 = 0;
      iVar13 = iVar14 + 1;
      pcVar10 = (char *)(iVar14 * 0xb + iVar6);
      do {
        if (*pcVar10 != -1) {
          *puVar9 = (ushort)(1 << (uVar11 & 0xff)) | *puVar9;
        }
        pcVar10 = pcVar10 + 1;
        uVar11 = uVar11 + 1;
      } while ((int)uVar11 < 10);
      iVar14 = iVar13;
    } while (iVar13 < 2);
    cleanup_card_actions();
    iVar14 = 0;
    if (0 < local_44) {
      do {
        uVar3 = (undefined1)auStack_84[iVar14];
        uVar4 = auStack_84[iVar14] >> 8;
        drawing_FUN_08022084(1,uVar3);
        drawing_FUN_08022034(0x4f,uVar3,uVar4);
        FUN_0802f73c(uVar3,uVar4,local_30);
        iVar14 = iVar14 + 1;
      } while (iVar14 < local_44);
    }
    process_card_actions();
    if (0 < local_44) {
      *(byte *)(DAT_08030090 + DAT_08030094) = *(byte *)(DAT_08030090 + DAT_08030094) | 3;
      uVar5 = 1;
      goto LAB_08030080;
    }
  }
  uVar5 = 0;
LAB_08030080:
  return CONCAT44(in_lr,uVar5);
}


// ===== 0803C484 FUN_0803c484

undefined8 FUN_0803c484(ushort *param_1)

{
  byte bVar1;
  uint uVar2;
  undefined4 uVar3;
  ushort *puVar4;
  char *pcVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  uint uVar9;
  int iVar10;
  undefined4 in_lr;
  bool bVar11;
  undefined8 uVar12;
  ushort auStack_30 [2];
  ushort *local_2c;
  int local_28;
  int local_24;
  
  local_2c = param_1;
  if ((param_1[1] & 8) == 0) {
    local_28 = 0;
    do {
      puVar4 = auStack_30 + local_28;
      *puVar4 = 0;
      uVar9 = 0;
      local_24 = local_28 + 1;
      pcVar5 = (char *)(local_28 * 0xb + DAT_0803c528 + DAT_0803c52c);
      do {
        if (*pcVar5 != -1) {
          *puVar4 = (ushort)(1 << (uVar9 & 0xff)) | *puVar4;
        }
        pcVar5 = pcVar5 + 1;
        uVar9 = uVar9 + 1;
      } while ((int)uVar9 < 10);
      local_28 = local_24;
    } while (local_24 < 2);
    if (*(char *)(DAT_0803c524 + DAT_0803c530) == '\x7f') {
      local_28 = 0;
      do {
        iVar10 = 5;
        local_24 = local_28 + 1;
        do {
          iVar7 = DAT_0803c8fc;
          iVar6 = DAT_0803c758;
          bVar1 = *(byte *)(local_28 * 0xb + iVar10 + DAT_0803c5e8 + DAT_0803c5ec);
          uVar9 = (uint)bVar1;
          if ((((uVar9 != 0xff) && (0x1a < (uVar9 & 0x7f) - 100)) &&
              (uVar2 = (uint)*local_2c, uVar9 != (uVar2 & 0x1ff) >> 1)) &&
             (iVar8 = (uVar9 & 0x7f) * 0x50 + DAT_0803c5f0 * (uint)(bVar1 >> 7) + DAT_0803c5e8,
             (int)((uint)*(byte *)(iVar8 + 0x33) * 0x8000000) < 0)) {
            bVar11 = false;
            uVar2 = (uint)*(ushort *)
                           ((*(ushort *)
                              (((uVar2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                               DAT_0803c5f0 * ((uVar2 & 0x1ff) >> 8) + DAT_0803c5e8 + 0x24) & 0x7fff
                            ) * 2 + DAT_0803c5f4);
            if (uVar2 == 0x1360) {
LAB_0803c658:
              iVar7 = (uVar9 & 0x7f) * 0x50 + DAT_0803c758 * ((int)(uVar9 & 0x80) >> 7) +
                      DAT_0803c75c;
              bVar11 = (*(uint *)((*(ushort *)(iVar7 + 0x24) & 0x7fff) * 4 + DAT_0803c760) &
                       0x1f00000) == 0x1600000;
              uVar2 = (uint)*(ushort *)((*(ushort *)(iVar7 + 0x24) & 0x7fff) * 2 + DAT_0803c5f4);
              if (((uVar2 == DAT_0803c764) || (uVar2 == DAT_0803c764 + 0xea)) &&
                 ((uVar2 = (uint)*(byte *)(iVar7 + 0x3c), uVar2 != 0xff &&
                  ((((*(uint *)((uVar2 & 0x7f) * 0x50 +
                                DAT_0803c758 * -((int)((uVar2 & 0x80) << 0x18) >> 0x1f) +
                                DAT_0803c75c + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0 &&
                   (*(char *)(iVar7 + 0x3d) == '\x01')))))) {
                bVar11 = true;
              }
              iVar8 = (uVar9 & 0x7f) * 0x50 + DAT_0803c758 * ((int)(uVar9 & 0x80) >> 7) +
                      DAT_0803c75c;
              iVar7 = FUN_080dce58(*(ushort *)(iVar8 + 0x24) & 0x7fff);
              if (((iVar7 != 0) &&
                  (((*(uint *)((*(byte *)(iVar8 + 0x3c) & 0x7f) * 0x50 +
                               iVar6 * -((int)((*(byte *)(iVar8 + 0x3c) & 0x80) << 0x18) >> 0x1f) +
                               DAT_0803c75c + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0)) &&
                 (*(char *)(iVar8 + 0x3d) == '\x02')) goto LAB_0803c880;
            }
            else if (uVar2 < 0x1361) {
              if (((uVar2 == 0x1296) || (uVar2 == 0x1302)) &&
                 ((undefined1 *)
                  (*(uint *)((*(ushort *)
                               ((uVar9 & 0x7f) * 0x50 + DAT_0803c64c * ((int)(uVar9 & 0x80) >> 7) +
                                DAT_0803c650 + 0x24) & 0x7fff) * 4 + DAT_0803c654) & 0x1f00000) ==
                  &DAT_01500000)) goto LAB_0803c880;
            }
            else if (uVar2 == DAT_0803c608) {
              uVar2 = (uint)*(ushort *)(iVar8 + 0x24);
              if (((*(uint *)((uVar2 & 0x7fff) * 4 + DAT_0803c8f8) & 0x1f00000) == 0x1600000) &&
                 ((*(uint *)((uVar2 & 0x7fff) * 4 + DAT_0803c8f8) & 0xe0000) == 0x60000)) {
                bVar11 = true;
              }
              iVar6 = (uVar9 & 0x7f) * 0x50 + DAT_0803c8fc * ((int)(uVar9 & 0x80) >> 7) +
                      DAT_0803c900;
              uVar2 = (uint)*(ushort *)((*(ushort *)(iVar6 + 0x24) & 0x7fff) * 2 + DAT_0803c5f4);
              if (((uVar2 == DAT_0803c904) || (uVar2 == DAT_0803c904 + 0xea)) &&
                 ((uVar2 = (uint)*(byte *)(iVar6 + 0x3c), uVar2 != 0xff &&
                  ((((*(uint *)((uVar2 & 0x7f) * 0x50 +
                                DAT_0803c8fc * -((int)((uVar2 & 0x80) << 0x18) >> 0x1f) +
                                DAT_0803c900 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0 &&
                   (*(char *)(iVar6 + 0x3d) == '\x01')))))) {
                bVar11 = true;
              }
              iVar8 = (uVar9 & 0x7f) * 0x50 + DAT_0803c8fc * ((int)(uVar9 & 0x80) >> 7) +
                      DAT_0803c900;
              iVar6 = FUN_080dce58(*(ushort *)(iVar8 + 0x24) & 0x7fff);
              if (((iVar6 != 0) &&
                  (((*(uint *)((*(byte *)(iVar8 + 0x3c) & 0x7f) * 0x50 +
                               iVar7 * -((int)((*(byte *)(iVar8 + 0x3c) & 0x80) << 0x18) >> 0x1f) +
                               DAT_0803c900 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0)) &&
                 (*(char *)(iVar8 + 0x3d) == '\x02')) {
                bVar11 = true;
              }
            }
            else if (uVar2 == DAT_0803c60c) goto LAB_0803c658;
            if (bVar11) {
LAB_0803c880:
              uVar12 = FUN_0800e158(uVar9,0x1f);
              return uVar12;
            }
          }
          iVar10 = iVar10 + 1;
        } while (iVar10 < 0xb);
        local_28 = local_24;
      } while (local_24 < 2);
      uVar3 = 10;
      goto LAB_0803c916;
    }
    if (*(char *)(DAT_0803c524 + DAT_0803c530) == -0x80) {
      uVar3 = 0x3b;
      if ((*local_2c & 1) != 0) {
        uVar3 = DAT_0803c534;
      }
      drawing_FUN_08022034(uVar3,(*local_2c & 0x1ff) >> 1,0x20);
      uVar3 = 0x7f;
      goto LAB_0803c916;
    }
    FUN_0802f9c4();
  }
  uVar3 = 0;
LAB_0803c916:
  return CONCAT44(in_lr,uVar3);
}


// ===== 08064FA8 FUN_08064fa8

uint FUN_08064fa8(undefined4 param_1,uint param_2)

{
  byte bVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  
  iVar5 = (param_2 & 0x7f) * 0x50 + DAT_08065044 * ((int)(param_2 & 0x80) >> 7) + DAT_08065040;
  uVar2 = *(uint *)(iVar5 + 0x30) & 0xfffff;
  uVar4 = uVar2 >> 0x13;
  uVar7 = uVar2 >> 0xc & 0x7f;
  uVar6 = (*(byte *)(iVar5 + 0x33) & 0x1f) >> 4;
  uVar2 = (*(byte *)(iVar5 + 0x33) & 0x3f) >> 5;
  uVar3 = (uint)*(ushort *)((*(ushort *)(iVar5 + 0x24) & 0x7fff) * 2 + DAT_08065048);
  if (uVar3 == DAT_0806504c) goto LAB_08065284;
  if ((int)uVar3 <= (int)DAT_0806504c) {
    if (uVar3 == DAT_0806504c - 0xa1) {
LAB_08065130:
      if ((*(uint *)((param_2 & 0x7f) * 0x50 + DAT_08065184 * ((int)(param_2 & 0x80) >> 7) +
                     DAT_08065040 + 0x30) & 0xfffff) >> 0x13 !=
          (*(byte *)(DAT_08065188 + DAT_08065040) & 3) >> 1) {
        return 0;
      }
    }
    else {
      if ((int)uVar3 <= (int)(DAT_0806504c - 0xa1)) {
        if (uVar3 == DAT_0806504c - 0x13f) {
          if (uVar7 != 5) {
            return 0;
          }
          bVar1 = *(byte *)(DAT_080651f0 + DAT_08065040);
        }
        else {
          if ((int)(DAT_0806504c - 0x13f) < (int)uVar3) {
            if (uVar3 != DAT_08065060) {
              if (uVar3 != DAT_08065060 + 0x80) {
                return 0;
              }
              goto LAB_08065130;
            }
          }
          else if ((uVar3 != DAT_0806504c - 0x20e) && (uVar3 != DAT_0806504c - 0x172)) {
            return 0;
          }
          if (((*(uint *)((*(byte *)(iVar5 + 0x3c) & 0x7f) * 0x50 +
                          DAT_080651d0 * (uint)(*(byte *)(iVar5 + 0x3c) >> 7) + DAT_08065040 + 0x30)
               & 0xfffff) >> 0xc & 0x7f) != 0) {
            return 0;
          }
          if (uVar7 != 5) {
            return 0;
          }
          bVar1 = *(byte *)(DAT_080651d4 + DAT_08065040);
        }
        if (uVar4 != 1 - ((bVar1 & 3) >> 1)) {
          return 0;
        }
        goto LAB_0806516c;
      }
      if (uVar3 == DAT_08065084) {
        if (uVar4 != (*(byte *)(DAT_08065264 + DAT_08065040) & 3) >> 1) {
          return 0;
        }
        if (uVar7 != 0) {
          return 0;
        }
        if (uVar6 == 0) {
          return 0;
        }
        goto joined_r0x0806527c;
      }
      if ((int)DAT_08065084 < (int)uVar3) {
        if (uVar3 == DAT_08065098) {
          if (uVar7 != 0) {
            return 0;
          }
          if (uVar4 != 1 - ((*(byte *)(DAT_08065220 + DAT_08065040) & 3) >> 1)) {
            return 0;
          }
          if (uVar6 == 0) {
            return 0;
          }
          uVar2 = FUN_08031174(param_1,param_2,2);
          return uVar2 & 0xffff;
        }
        uVar2 = DAT_080650a0;
        if ((int)uVar3 <= (int)DAT_08065098) {
          uVar2 = DAT_08065098 - 0x31;
          goto LAB_08065122;
        }
        goto LAB_08065112;
      }
      if (uVar3 != DAT_08065084 - 0x4b) {
        if (uVar3 != DAT_08065084 - 1) {
          return 0;
        }
        if (uVar4 != (*(byte *)(DAT_08065240 + DAT_08065040) & 3) >> 1) {
          return 0;
        }
        if (uVar7 != 0) {
          return 0;
        }
        if (uVar6 != 0) {
          if (uVar2 == 0) {
            return 1;
          }
          return 0;
        }
        return 0;
      }
    }
    if (uVar7 != 5) {
      return 0;
    }
LAB_0806516c:
    if (uVar6 == 0) {
      return 0;
    }
    uVar2 = FUN_0800e158(param_2,0x1f);
    return uVar2;
  }
  if (uVar3 == DAT_080650c8) goto LAB_08065284;
  if ((int)uVar3 <= (int)DAT_080650c8) {
    if (uVar3 == DAT_080650c8 - 0xa9) goto LAB_08065284;
    if ((int)(DAT_080650c8 - 0xa9) < (int)uVar3) {
      if (uVar3 == DAT_080650dc) goto LAB_08065268;
      if ((int)uVar3 <= (int)DAT_080650dc) {
        uVar2 = DAT_080650dc - 0x2b;
        goto LAB_08065122;
      }
      uVar2 = 0x15a0;
    }
    else {
      if (uVar3 == DAT_080650c8 - 0x13c) goto LAB_08065284;
      uVar2 = DAT_080650c8 - 0xae;
    }
LAB_08065112:
    if (uVar3 != uVar2) {
      return 0;
    }
LAB_08065284:
    if (((uVar7 == 5) && (uVar4 == (*(byte *)(DAT_080652ac + DAT_08065040) & 3) >> 1)) &&
       (uVar6 != 0)) {
      uVar2 = FUN_0800e158(param_2,0x1f);
      return uVar2;
    }
    return 0;
  }
  if (uVar3 != DAT_08065100) {
    if ((int)DAT_08065100 < (int)uVar3) {
      if (uVar3 != DAT_0806511c) {
        uVar2 = DAT_0806512c;
        if ((int)uVar3 <= (int)DAT_0806511c) {
          uVar2 = DAT_0806511c - 0x1f;
          goto LAB_08065112;
        }
        goto LAB_08065122;
      }
    }
    else if (uVar3 != DAT_08065100 - 199) {
      uVar2 = DAT_08065100 - 0xb9;
LAB_08065122:
      if (uVar3 != uVar2) {
        return 0;
      }
    }
  }
LAB_08065268:
  if (uVar4 != (*(byte *)(DAT_08065280 + DAT_08065040) & 3) >> 1) {
    return 0;
  }
  uVar2 = uVar6;
  if (uVar7 != 0) {
    return 0;
  }
joined_r0x0806527c:
  if (uVar2 == 0) {
    return 0;
  }
  return 1;
}


// ===== 08032640 FUN_08032640

undefined8 FUN_08032640(ushort *param_1,ushort *param_2)

{
  byte bVar1;
  byte bVar2;
  ushort *puVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  undefined4 in_lr;
  
  if (param_2 != (ushort *)0x0) {
    bVar1 = (byte)*param_2;
    bVar2 = (byte)*param_1;
    if ((bVar1 & 1) != (bVar2 & 1)) {
      uVar6 = (uint)*(ushort *)
                     ((*(ushort *)
                        (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         DAT_080326d0 * ((*param_1 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) & 0x7fff) *
                      2 + DAT_080326d8);
      if (uVar6 == DAT_080326dc) {
        iVar5 = FUN_080dced4(*(ushort *)
                              (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                               DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) &
                             0x7fff);
        if (iVar5 != 0) goto LAB_08032cc4;
      }
      else {
        if ((int)uVar6 <= (int)DAT_080326dc) {
          if (uVar6 == DAT_080326e0) {
            puVar3 = (ushort *)
                     ((*(ushort *)
                        (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) & 0x7fff) *
                      2 + DAT_080327b8);
            uVar6 = DAT_080327bc;
          }
          else if ((int)DAT_080326e0 < (int)uVar6) {
            if (uVar6 == DAT_080326f4) {
              puVar3 = (ushort *)
                       ((*(ushort *)
                          (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) & 0x7fff)
                        * 2 + DAT_080327f0);
              uVar6 = DAT_080327f4;
            }
            else {
              if (uVar6 != DAT_080326f4 + 0x25) goto LAB_08032cd0;
              puVar3 = (ushort *)
                       ((*(ushort *)
                          (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) & 0x7fff)
                        * 2 + DAT_08032834);
              uVar6 = DAT_08032838;
            }
          }
          else {
            if (uVar6 == DAT_080326e0 - 0x1c) {
              uVar6 = (uint)*(ushort *)
                             ((*(ushort *)
                                (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                 DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) &
                              0x7fff) * 2 + DAT_08032890);
              if (uVar6 != DAT_08032894) {
                if ((int)DAT_08032894 < (int)uVar6) {
                  uVar4 = DAT_080328d8;
                  if ((int)uVar6 <= DAT_080328d0) {
                    if ((DAT_080328d0 + -1 <= (int)uVar6) || (uVar6 == DAT_080328d0 - 0x2bU))
                    goto LAB_08032cc4;
                    uVar4 = DAT_080328d0 - 0x1e;
                  }
LAB_080328c8:
                  if (uVar6 != uVar4) goto LAB_08032cd0;
                }
                else if (uVar6 != DAT_08032894 - 0x20) {
                  iVar5 = DAT_080328ac;
                  if ((int)(DAT_08032894 - 0x20) < (int)uVar6) goto LAB_0803289a;
                  if (uVar6 < 0x1101) {
                    iVar5 = 0x10f8;
                    goto LAB_080328a2;
                  }
                  goto LAB_08032cd0;
                }
              }
              goto LAB_08032cc4;
            }
            if (uVar6 != DAT_080326e0 - 1) goto LAB_08032cd0;
            puVar3 = (ushort *)
                     ((*(ushort *)
                        (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) & 0x7fff) *
                      2 + DAT_08032780);
            uVar6 = DAT_08032784;
          }
          uVar6 = (uint)(*puVar3 == uVar6);
          goto LAB_08032cd2;
        }
        if (uVar6 == DAT_08032718) {
          if ((((bVar2 & 1) != (bVar1 & 1)) &&
              ((undefined1 *)
               (*(uint *)((*(ushort *)
                            (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                             DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) &
                          0x7fff) * 4 + DAT_08032b6c) & 0x1f00000) == &DAT_01500000)) &&
             ((*(byte *)(DAT_08032b70 + DAT_080326d4) & 0x1c) == 0xc)) goto LAB_08032cc4;
        }
        else {
          if ((int)uVar6 <= (int)DAT_08032718) {
            if (uVar6 == DAT_0803271c) {
              uVar6 = (uint)*(ushort *)
                             ((*(ushort *)
                                (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                 DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) &
                              0x7fff) * 2 + DAT_0803297c);
              if (uVar6 != DAT_08032980) {
                if ((int)DAT_08032980 < (int)uVar6) {
                  if (uVar6 != DAT_08032a1c) {
                    if ((int)DAT_08032a1c < (int)uVar6) {
                      if (uVar6 != DAT_08032a64) {
                        if ((int)DAT_08032a64 < (int)uVar6) {
                          if (uVar6 != DAT_08032a90) {
                            if ((int)DAT_08032a90 < (int)uVar6) {
                              uVar4 = DAT_08032aa4;
                              if (uVar6 != DAT_08032aa0) goto LAB_080328c8;
                            }
                            else if (uVar6 != DAT_08032a90 - 9) {
                              uVar4 = DAT_08032a90 - 2;
                              goto LAB_080328c8;
                            }
                          }
                        }
                        else if (uVar6 != DAT_08032a64 - 0x39) {
                          if ((int)(DAT_08032a64 - 0x39) < (int)uVar6) {
                            if ((int)uVar6 <= DAT_08032a74) {
                              iVar5 = DAT_08032a74 + -3;
                              goto LAB_080328a2;
                            }
                            goto LAB_08032cd0;
                          }
                          uVar4 = DAT_08032a64 - 0x5f;
                          goto LAB_080328c8;
                        }
                      }
                    }
                    else if (uVar6 != DAT_08032a1c - 0x6c) {
                      if ((int)(DAT_08032a1c - 0x6c) < (int)uVar6) {
                        uVar4 = DAT_08032a44;
                        if ((int)uVar6 <= DAT_08032a3c) {
                          if (DAT_08032a3c + -1 <= (int)uVar6) goto LAB_08032cc4;
                          uVar4 = DAT_08032a3c - 9;
                        }
                      }
                      else {
                        if (uVar6 == DAT_08032a1c - 0x9b) goto LAB_08032cc4;
                        uVar4 = DAT_08032a24;
                        if ((int)uVar6 <= (int)(DAT_08032a1c - 0x9b)) {
                          iVar5 = DAT_08032a1c - 0xd4;
                          goto LAB_0803289a;
                        }
                      }
                      goto LAB_080328c8;
                    }
                  }
                }
                else if ((int)(DAT_08032980 - 0x37) < (int)uVar6) {
                  if (DAT_080329cc < (int)uVar6) {
                    if (uVar6 != DAT_080329e8) {
                      uVar4 = DAT_080329f0;
                      if ((int)uVar6 <= (int)DAT_080329e8) {
                        uVar4 = DAT_080329e8 - 2;
                      }
                      goto LAB_080328c8;
                    }
                  }
                  else if (((int)uVar6 < DAT_080329cc + -1) && (uVar6 != DAT_080329cc - 0x12U)) {
                    iVar5 = DAT_080329d4;
                    if ((int)(DAT_080329cc - 0x12U) < (int)uVar6) {
LAB_0803289a:
                      if ((int)uVar6 <= iVar5) {
                        iVar5 = iVar5 + -1;
LAB_080328a2:
                        if (iVar5 <= (int)uVar6) goto LAB_08032cc4;
                      }
                      goto LAB_08032cd0;
                    }
                    uVar4 = DAT_080329cc - 0x16;
                    goto LAB_080328c8;
                  }
                }
                else if (((int)uVar6 < (int)(DAT_08032980 - 0x38)) && (uVar6 != DAT_08032980 - 0xf4)
                        ) {
                  if ((int)uVar6 <= (int)(DAT_08032980 - 0xf4)) {
                    if (DAT_08032984 <= (int)uVar6) {
                      if ((int)uVar6 <= DAT_08032984 + 0x10) goto LAB_08032cc4;
                      if ((int)uVar6 <= DAT_08032984 + 0x1b) {
                        iVar5 = DAT_08032984 + 0x12;
                        goto LAB_080328a2;
                      }
                    }
                    goto LAB_08032cd0;
                  }
                  if (uVar6 != DAT_08032998) {
                    if ((int)DAT_08032998 < (int)uVar6) {
                      if (uVar6 == DAT_080329a8) goto LAB_08032cc4;
                      uVar4 = DAT_080329a8 + 0x24;
                    }
                    else {
                      uVar4 = DAT_08032998 - 3;
                    }
                    goto LAB_080328c8;
                  }
                }
              }
            }
            else {
              if (uVar6 != DAT_0803271c + 0xb2) goto LAB_08032cd0;
              uVar6 = (uint)*(ushort *)
                             ((*(ushort *)
                                (((*param_2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                 DAT_080326d0 * ((*param_2 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) &
                              0x7fff) * 2 + DAT_08032aec);
              if (uVar6 != DAT_08032af0) {
                if ((int)DAT_08032af0 < (int)uVar6) {
                  if ((int)uVar6 < DAT_08032b08) goto LAB_08032cd0;
                  if (DAT_08032b08 + 1 < (int)uVar6) {
                    uVar4 = DAT_08032b08 + 0x30;
                    goto LAB_080328c8;
                  }
                }
                else if (uVar6 != DAT_08032af0 - 0x47) {
                  uVar4 = DAT_08032af0 - 0x42;
                  goto LAB_080328c8;
                }
              }
            }
LAB_08032cc4:
            uVar6 = 1;
            goto LAB_08032cd2;
          }
          if (uVar6 == DAT_08032738) {
            if (((bVar2 & 1) != (bVar1 & 1)) &&
               (uVar6 = (uint)*param_2,
               (*(uint *)((*(ushort *)
                            (((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                             DAT_080326d0 * ((uVar6 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) & 0x7fff)
                          * 4 + DAT_08032c50) & 0x1f00000) == 0x1600000)) {
              iVar7 = ((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 + DAT_080326d0 * ((uVar6 & 0x1ff) >> 8) +
                      DAT_080326d4;
              iVar5 = DAT_08032c50;
LAB_08032cae:
              if ((*(uint *)((*(ushort *)(iVar7 + 0x24) & 0x7fff) * 4 + iVar5) & 0xe0000) == 0x80000
                 ) goto LAB_08032cc4;
            }
          }
          else if ((int)DAT_08032738 < (int)uVar6) {
            if (((uVar6 == DAT_0803274c) && ((bVar2 & 1) != (bVar1 & 1))) &&
               (uVar6 = (uint)*param_2,
               (undefined1 *)
               (*(uint *)((*(ushort *)
                            (((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                             DAT_080326d0 * ((uVar6 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) & 0x7fff)
                          * 4 + DAT_08032cc8) & 0x1f00000) == &DAT_01500000)) {
              iVar7 = ((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 + DAT_080326d0 * ((uVar6 & 0x1ff) >> 8) +
                      DAT_08032ccc;
              iVar5 = DAT_08032cc8;
              goto LAB_08032cae;
            }
          }
          else if (((uVar6 == DAT_0803273c) &&
                   (uVar6 = (uint)*param_2,
                   (*(uint *)((*(ushort *)
                                (((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                 DAT_080326d0 * ((uVar6 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) &
                              0x7fff) * 4 + DAT_08032be4) & 0x1f00000) == 0x1600000)) &&
                  ((*(uint *)((*(ushort *)
                                (((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                 DAT_080326d0 * ((uVar6 & 0x1ff) >> 8) + DAT_080326d4 + 0x24) &
                              0x7fff) * 4 + DAT_08032be4) & 0xe0000) == 0x60000)) goto LAB_08032cc4;
        }
      }
    }
  }
LAB_08032cd0:
  uVar6 = 0;
LAB_08032cd2:
  return CONCAT44(in_lr,uVar6);
}


// ===== 08019BDC FUN_08019bdc

/* WARNING: Removing unreachable block (ram,0x0801a106) */

undefined8 FUN_08019bdc(uint param_1,uint param_2,short param_3,short param_4)

{
  byte bVar1;
  bool bVar2;
  int iVar3;
  uint uVar4;
  undefined4 uVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  byte *pbVar9;
  int iVar10;
  undefined4 in_lr;
  undefined8 uVar11;
  
  if (param_3 == 0) {
    FUN_08019884(param_2);
    iVar3 = (param_2 & 0x7f) * 0x50 + DAT_08019c4c * ((int)(param_2 & 0x80) >> 7) + DAT_08019c48;
    uVar6 = (uint)*(ushort *)((*(ushort *)(iVar3 + 0x24) & 0x7fff) * 2 + DAT_08019c44);
    if (uVar6 == DAT_08019c50) {
LAB_08019c90:
      uVar6 = 0xffffffff;
      iVar3 = 5;
      pbVar9 = (byte *)(((int)(param_2 & 0x80) >> 7) * 0xb + DAT_08019ce8 + DAT_08019cec);
      do {
        if (*pbVar9 == param_2) {
          uVar6 = iVar3 - 5;
        }
        pbVar9 = pbVar9 + 1;
        iVar3 = iVar3 + 1;
      } while (iVar3 < 10);
      if (uVar6 == 0xffffffff) {
        uVar6 = *(uint *)((param_2 & 0x7f) * 0x50 + DAT_08019cf0 * ((int)(param_2 & 0x80) >> 7) +
                          DAT_08019ce8 + 0x30);
LAB_08019d1a:
        uVar11 = send_card_to_graveyard
                           (param_2,((uVar6 & 0xfffff) >> 0x13) << 0xf | 0x41,param_2 & 0xffff);
        return uVar11;
      }
      FUN_080188ac(param_2,((param_2 & 0x80) >> 7) << 0xf | (uVar6 & 0x3f) << 4 | 0x1400);
    }
    else if ((int)DAT_08019c50 < (int)uVar6) {
      if (uVar6 == DAT_08019c78) {
LAB_08019c88:
        FUN_080197a8(param_2);
      }
      else if ((int)DAT_08019c78 < (int)uVar6) {
        if (uVar6 == DAT_08019c84) {
          uVar6 = *(uint *)(iVar3 + 0x30);
          goto LAB_08019d1a;
        }
      }
      else if (uVar6 == DAT_08019c78 - 0x6a) {
        bVar2 = true;
        iVar3 = 0;
        do {
          iVar10 = 0;
          if (bVar2) {
            pbVar9 = (byte *)(iVar3 * 0xb + DAT_08019eec + DAT_08019ef4);
            do {
              uVar6 = (uint)*pbVar9;
              if ((((uVar6 != 0xff) && (uVar6 != param_2)) && (0x1a < (uVar6 & 0x7f) - 100)) &&
                 ((iVar7 = (uVar6 & 0x7f) * 0x50 + (uint)(*pbVar9 >> 7) * DAT_08019ef8 +
                           DAT_08019eec,
                  *(ushort *)((*(ushort *)(iVar7 + 0x24) & 0x7fff) * 2 + DAT_08019ef0) ==
                  DAT_08019efc && ((int)((uint)*(byte *)(iVar7 + 0x33) * 0x8000000) < 0)))) {
                bVar2 = false;
              }
              pbVar9 = pbVar9 + 1;
              iVar10 = iVar10 + 1;
            } while ((iVar10 < 5) && (bVar2));
          }
        } while ((iVar3 + 1 < 2) && (iVar3 = iVar3 + 1, bVar2));
        if (bVar2) {
          iVar3 = 0;
          do {
            iVar7 = 0;
            iVar10 = iVar3 + 1;
            do {
              bVar1 = *(byte *)(iVar3 * 0xb + iVar7 + DAT_08019ef4 + DAT_08019eec);
              uVar6 = (uint)bVar1;
              if ((((uVar6 != 0xff) && (0x1a < (uVar6 & 0x7f) - 100)) &&
                  (iVar8 = (uVar6 & 0x7f) * 0x50 + DAT_08019ef8 * (uint)(bVar1 >> 7) + DAT_08019eec,
                  *(ushort *)((*(ushort *)(iVar8 + 0x24) & 0x7fff) * 2 + DAT_08019ef0) ==
                  DAT_08019f00)) && ((int)((uint)*(byte *)(iVar8 + 0x33) * 0x8000000) < 0)) {
                uVar11 = send_card_to_graveyard
                                   (uVar6,((*(uint *)((param_2 & 0x7f) * 0x50 +
                                                      DAT_08019ef8 * ((int)(param_2 & 0x80) >> 7) +
                                                      DAT_08019eec + 0x30) & 0xfffff) >> 0xc & 0x80)
                                          << 8 | 0x41,param_2 & 0xffff);
                return uVar11;
              }
              iVar7 = iVar7 + 1;
            } while (iVar7 < 5);
            iVar3 = iVar10;
          } while (iVar10 < 2);
        }
      }
    }
    else {
      if (uVar6 == DAT_08019c54) goto LAB_08019c90;
      if ((int)DAT_08019c54 < (int)uVar6) {
        if (uVar6 == DAT_08019c60) goto LAB_08019c90;
      }
      else if (uVar6 == DAT_08019c54 - 0x40) goto LAB_08019c88;
    }
    iVar10 = (int)(param_2 & 0x80) >> 7;
    iVar3 = FUN_080dce58(*(ushort *)
                          ((param_2 & 0x7f) * 0x50 + iVar10 * DAT_08019ef8 + DAT_08019eec + 0x24) &
                         0x7fff);
    if (iVar3 != 0) {
      uVar5 = 0x3b;
      if (iVar10 != 0) {
        uVar5 = DAT_08019f04;
      }
      drawing_FUN_08022034(uVar5,param_2 & 0xffff,0x13);
    }
    FUN_08018794(param_2);
    iVar10 = (int)(param_2 & 0x80) >> 7;
    iVar3 = FUN_080dce58(*(ushort *)
                          ((param_2 & 0x7f) * 0x50 + iVar10 * DAT_08019ef8 + DAT_08019eec + 0x24) &
                         0x7fff);
    if (iVar3 != 0) {
      uVar5 = 0x3b;
      if (iVar10 != 0) {
        uVar5 = DAT_08019f04;
      }
      drawing_FUN_08022034(uVar5,param_2 & 0xffff,0x13);
    }
LAB_0801a292:
    uVar5 = 0;
  }
  else {
    if (param_4 == 0) {
LAB_08019f68:
      iVar3 = (param_2 & 0x7f) * 0x50 + DAT_08019fb0 * ((int)(param_2 & 0x80) >> 7) + DAT_08019fac;
      uVar6 = (uint)*(ushort *)((*(ushort *)(iVar3 + 0x24) & 0x7fff) * 2 + DAT_08019fa8);
      if (uVar6 == DAT_08019fb4) {
        iVar7 = 0;
        iVar10 = DAT_08019fb0;
        while( true ) {
          if ((int)((*(uint *)(iVar10 * ((*(uint *)(iVar3 + 0x30) & 0xfffff) >> 0x13) + DAT_08019fac
                              + 0x1c) & 0xfffff) >> 0xd) <= iVar7) {
            uVar11 = send_card_to_graveyard
                               (param_2,((*(uint *)((param_1 & 0x7f) * 0x50 +
                                                    ((int)(param_1 & 0x80) >> 7) * DAT_0801a144 +
                                                    DAT_08019fac + 0x30) & 0xfffff) >> 0x13) << 0xf
                                        | DAT_0801a148,param_2 & 0xffff);
            return uVar11;
          }
          uVar6 = (uint)*(byte *)(iVar10 * ((*(uint *)(iVar3 + 0x30) & 0xfffff) >> 0x13) + iVar7 +
                                 DAT_0801a08c + DAT_08019fac);
          if ((uVar6 != param_2) &&
             (uVar6 = (uint)*(ushort *)
                             ((*(ushort *)
                                ((uVar6 & 0x7f) * 0x50 + iVar10 * ((int)(uVar6 & 0x80) >> 7) +
                                 DAT_08019fac + 0x24) & 0x7fff) * 2 + DAT_0801a090) + DAT_0801a094,
             uVar6 < 5)) break;
          iVar7 = iVar7 + 1;
          iVar3 = (param_2 & 0x7f) * 0x50 + DAT_0801a144 * ((int)(param_2 & 0x80) >> 7) +
                  DAT_08019fac;
          iVar10 = DAT_0801a144;
        }
                    /* WARNING: Could not recover jumptable at 0x0801a08a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
        uVar11 = (**(code **)(uVar6 * 4 + DAT_0801a098))();
        return uVar11;
      }
      if ((int)DAT_08019fb4 < (int)uVar6) {
        if (uVar6 != DAT_08019fd8) {
          uVar4 = DAT_08019fdc;
          if ((int)DAT_08019fd8 < (int)uVar6) {
            if (uVar6 == DAT_08019fec) {
              bVar2 = true;
              iVar3 = 0;
              do {
                iVar10 = 0;
                if (bVar2) {
                  pbVar9 = (byte *)(iVar3 * 0xb + DAT_0801a2a4 + DAT_0801a2ac);
                  do {
                    uVar6 = (uint)*pbVar9;
                    if ((((uVar6 != 0xff) && (uVar6 != param_2)) && (0x1a < (uVar6 & 0x7f) - 100))
                       && ((iVar7 = (uVar6 & 0x7f) * 0x50 + (uint)(*pbVar9 >> 7) * DAT_0801a2b0 +
                                    DAT_0801a2a4,
                           *(ushort *)((*(ushort *)(iVar7 + 0x24) & 0x7fff) * 2 + DAT_0801a2a8) ==
                           DAT_0801a2b4 && ((int)((uint)*(byte *)(iVar7 + 0x33) * 0x8000000) < 0))))
                    {
                      bVar2 = false;
                    }
                    pbVar9 = pbVar9 + 1;
                    iVar10 = iVar10 + 1;
                  } while ((iVar10 < 5) && (bVar2));
                }
              } while ((iVar3 + 1 < 2) && (iVar3 = iVar3 + 1, bVar2));
              if (bVar2) {
                iVar3 = 0;
                do {
                  iVar10 = 0;
                  iVar7 = iVar3 + 1;
                  do {
                    bVar1 = *(byte *)(iVar3 * 0xb + iVar10 + DAT_0801a2a4 + DAT_0801a2ac);
                    uVar6 = (uint)bVar1;
                    if ((((uVar6 != 0xff) && (0x1a < (uVar6 & 0x7f) - 100)) &&
                        (iVar8 = (uVar6 & 0x7f) * 0x50 + DAT_0801a2b0 * (uint)(bVar1 >> 7) +
                                 DAT_0801a2a4,
                        *(ushort *)((*(ushort *)(iVar8 + 0x24) & 0x7fff) * 2 + DAT_0801a2a8) ==
                        DAT_0801a2b8)) && ((int)((uint)*(byte *)(iVar8 + 0x33) * 0x8000000) < 0)) {
                      uVar11 = send_card_to_graveyard
                                         (uVar6,((*(uint *)((param_2 & 0x7f) * 0x50 +
                                                            DAT_0801a2b0 *
                                                            ((int)(param_2 & 0x80) >> 7) +
                                                            DAT_0801a2a4 + 0x30) & 0xfffff) >> 0xc &
                                                0x80) << 8 | 0x41,param_2 & 0xffff);
                      return uVar11;
                    }
                    iVar10 = iVar10 + 1;
                  } while (iVar10 < 5);
                  iVar3 = iVar7;
                } while (iVar7 < 2);
              }
            }
            goto LAB_0801a292;
          }
          goto LAB_08019fd0;
        }
      }
      else if (uVar6 != DAT_08019fb8) {
        uVar4 = DAT_08019fc0;
        if ((int)uVar6 <= (int)DAT_08019fb8) {
          uVar4 = DAT_08019fb8 - 6;
        }
LAB_08019fd0:
        if (uVar6 != uVar4) goto LAB_0801a292;
      }
      uVar6 = *(uint *)((param_2 & 0x7f) * 0x50 + DAT_0801a030 * ((int)(param_2 & 0x80) >> 7) +
                        DAT_08019fac + 0x30);
    }
    else {
      iVar10 = (param_2 & 0x7f) * 0x50 + DAT_08019f60 * ((int)(param_2 & 0x80) >> 7) + DAT_08019f5c;
      iVar3 = FUN_080dced4(*(ushort *)(iVar10 + 0x24) & 0x7fff);
      if ((iVar3 == 0) ||
         (iVar3 = show_confirmation_prompt(DAT_08019f64,0xff,3,0x20,0x10e,1), iVar3 != 0))
      goto LAB_08019f68;
      uVar6 = *(uint *)(iVar10 + 0x30);
    }
    FUN_080314b4(((uVar6 & 0xfffff) >> 0x13) << 0x1f | param_2 & 0xff | 0x16600000,0);
    uVar5 = 1;
  }
  return CONCAT44(in_lr,uVar5);
}


// ===== 0807375C FUN_0807375c

undefined8 FUN_0807375c(ushort param_1)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  uint uVar5;
  int iVar6;
  undefined4 in_lr;
  ushort local_24 [12];
  
  iVar2 = DAT_08073808;
  local_24[0] = local_24[0] | 1;
  local_24[0] = (ushort)DAT_080737bc & local_24[0] | (param_1 & 0xff) << 1;
  uVar5 = (uint)*(ushort *)
                 ((*(ushort *)
                    ((param_1 & 0x7f) * 0x50 + ((param_1 & 0x80) >> 7) * DAT_080737c8 + DAT_080737c4
                    + 0x24) & 0x7fff) * 2 + DAT_080737c0);
  if (uVar5 != DAT_080737cc) {
    uVar1 = DAT_080737dc;
    if ((int)uVar5 <= (int)DAT_080737cc) {
      uVar1 = DAT_080737cc - 0x44;
    }
    if (uVar5 != uVar1) {
      iVar6 = 0;
      do {
        if ((*(char *)(iVar6 + iVar2) != -1) && (iVar3 = FUN_080616b8(local_24), iVar3 != 0))
        goto LAB_080737d6;
        iVar6 = iVar6 + 1;
      } while (iVar6 < 5);
      uVar4 = 0;
      goto LAB_080737fe;
    }
  }
LAB_080737d6:
  uVar4 = 1;
LAB_080737fe:
  return CONCAT44(in_lr,uVar4);
}


// ===== 080738B4 FUN_080738b4

undefined8 FUN_080738b4(int param_1,uint param_2)

{
  short sVar1;
  uint uVar2;
  uint uVar3;
  undefined4 uVar4;
  char *pcVar5;
  int iVar6;
  undefined4 in_lr;
  
  if ((param_2 != 0xff) && (0x1a < (param_2 & 0x7f) - 100)) {
    iVar6 = (param_2 & 0x7f) * 0x50 + DAT_0807396c * ((int)(param_2 & 0x80) >> 7) + DAT_08073968;
    uVar2 = (uint)*(ushort *)(iVar6 + 0x24);
    if (((*(uint *)((uVar2 & 0x7fff) * 4 + DAT_08073964) & 0x1f00000) != 0x1600000) ||
       (((*(uint *)((uVar2 & 0x7fff) * 4 + DAT_08073964) & 0xe0000) != 0x40000 ||
        (uVar2 = FUN_08011270(),
        uVar2 != *(ushort *)((*(ushort *)(iVar6 + 0x24) & 0x7fff) * 2 + DAT_08073970))))) {
      iVar6 = (param_2 & 0x7f) * 0x50 + DAT_0807396c * ((int)(param_2 & 0x80) >> 7) + DAT_08073968;
      uVar2 = (uint)*(ushort *)((*(ushort *)(iVar6 + 0x24) & 0x7fff) * 2 + DAT_08073970);
      if (uVar2 == DAT_08073974) {
LAB_080739c2:
        iVar6 = 5;
        pcVar5 = (char *)(DAT_080739e8 + (1 - param_1) * 0xb + DAT_080739ec);
        do {
          if (*pcVar5 != -1) goto LAB_08073a4e;
          pcVar5 = pcVar5 + 1;
          iVar6 = iVar6 + 1;
        } while (iVar6 < 0xb);
      }
      else if ((int)DAT_08073974 < (int)uVar2) {
        if (uVar2 == DAT_08073998) goto LAB_080739c2;
        if ((int)uVar2 <= (int)DAT_08073998) {
          uVar3 = DAT_08073998 - 0xb;
          goto LAB_08073990;
        }
        if ((uVar2 != DAT_080739a4) ||
           (DAT_08073a00 < *(uint *)(DAT_0807396c * param_1 + DAT_08073968))) goto LAB_08073a4e;
      }
      else if (uVar2 == DAT_08073974 - 0x31) {
        sVar1 = FUN_0807380c(0xff);
        if (sVar1 == 0) {
          FUN_08072ecc(*(ushort *)(iVar6 + 0x24) & 0x7fff,0);
        }
      }
      else {
        uVar3 = DAT_08073980;
        if ((int)(DAT_08073974 - 0x31) < (int)uVar2) {
LAB_08073990:
          if ((uVar2 != uVar3) ||
             ((sVar1 = FUN_0807380c(0xff), sVar1 == 0 &&
              (-1 < (int)((uint)*(byte *)(param_1 * DAT_08073a2c + DAT_08073a28 + DAT_08073a30) *
                         0x2000000))))) goto LAB_08073a4e;
        }
        else if ((uVar2 != DAT_08073978) ||
                ((sVar1 = FUN_0807380c(0xff), sVar1 == 0 &&
                 (iVar6 = FUN_08010bec(1 - param_1), iVar6 != 0)))) {
LAB_08073a4e:
          uVar4 = 1;
          goto LAB_08073a50;
        }
      }
    }
  }
  uVar4 = 0;
LAB_08073a50:
  return CONCAT44(in_lr,uVar4);
}



// ===== 08039300 FUN_08039300

longlong FUN_08039300(byte *param_1)

{
  undefined4 uVar1;
  uint in_lr;
  
  uVar1 = 0x24;
  if ((*param_1 & 1) != 0) {
    uVar1 = DAT_0803931c;
  }
  drawing_FUN_080220d4(uVar1);
  return (ulonglong)in_lr << 0x20;
}


// ===== 08039320 FUN_08039320

longlong FUN_08039320(ushort *param_1)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  uint in_lr;
  
  iVar5 = 0;
  if ((param_1[1] & 8) != 0) goto LAB_08039458;
  uVar3 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                     DAT_08039390 * ((*param_1 & 0x1ff) >> 8) + DAT_0803938c + 0x24) & 0x7fff) * 2 +
                 DAT_08039388);
  if (uVar3 == DAT_08039394) {
LAB_080393fc:
    iVar5 = 1;
  }
  else {
    if ((int)uVar3 <= (int)DAT_08039394) {
      if (uVar3 != DAT_08039398) {
        if ((int)DAT_08039398 < (int)uVar3) {
          if (uVar3 != DAT_080393b0) {
            uVar2 = DAT_080393b8;
            if ((int)uVar3 <= (int)DAT_080393b0) {
              uVar2 = DAT_080393b0 - 0xbb;
            }
            goto LAB_080393e4;
          }
        }
        else if (uVar3 != DAT_0803939c) {
          if (uVar3 != DAT_0803939c + 0xf3) goto LAB_08039448;
          goto LAB_08039400;
        }
      }
      goto LAB_080393fc;
    }
    if (uVar3 == DAT_080393d0) {
LAB_08039400:
      iVar5 = 2;
    }
    else if ((int)DAT_080393d0 < (int)uVar3) {
      if (uVar3 == DAT_080393ec) goto LAB_080393fc;
      if ((int)uVar3 <= (int)DAT_080393ec) {
        uVar2 = DAT_080393ec - 4;
        goto LAB_080393e4;
      }
      if (uVar3 == DAT_080393f8) {
        iVar5 = (*(byte *)((int)param_1 + 9) & 1) + 1;
      }
    }
    else if (uVar3 == DAT_080393d4) {
      iVar1 = (int)((uint)(byte)*param_1 << 0x1f) >> 0x1f;
      iVar4 = DAT_08039390 * -iVar1 + DAT_0803938c;
      if ((byte)((*(byte *)(iVar4 + 0x1c) & 0x3f) << 1 | *(byte *)(iVar4 + 0x1b) >> 7) < 2) {
        iVar5 = DAT_08039390 * -iVar1 + DAT_0803938c;
        iVar5 = 2 - ((*(byte *)(iVar5 + 0x1c) & 0x3f) << 1 | (uint)(*(byte *)(iVar5 + 0x1b) >> 7));
      }
    }
    else {
      uVar2 = DAT_080393d4 + 0xb3;
LAB_080393e4:
      if (uVar3 == uVar2) goto LAB_080393fc;
    }
LAB_08039448:
    if (iVar5 < 1) goto LAB_08039458;
  }
  FUN_0801b28c((byte)*param_1 & 1,iVar5);
LAB_08039458:
  return (ulonglong)in_lr << 0x20;
}


// ===== 0803A48C FUN_0803a48c

longlong FUN_0803a48c(ushort *param_1)

{
  int iVar1;
  ushort uVar2;
  uint uVar3;
  undefined4 uVar4;
  uint uVar5;
  int iVar6;
  int iVar7;
  uint in_lr;
  
  if ((param_1[1] & 8) != 0) goto LAB_0803a85e;
  uVar3 = (uint)*param_1;
  uVar5 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((uVar3 & 0x1ff) >> 1 & 0x7f) * 0x50 + ((uVar3 & 0x1ff) >> 8) * DAT_0803a514 +
                     DAT_0803a510 + 0x24) & 0x7fff) * 2 + DAT_0803a50c);
  if (uVar5 == DAT_0803a518) {
LAB_0803a61e:
    uVar3 = 1 - ((byte)*param_1 & 1);
LAB_0803a6a4:
    FUN_0801abf0(uVar3,500);
    goto LAB_0803a85e;
  }
  if ((int)DAT_0803a518 < (int)uVar5) {
    if (uVar5 == DAT_0803a594) {
      FUN_0801abf0(1 - ((byte)*param_1 & 1),500);
      FUN_0801ad6c((byte)*param_1 & 1,500);
      goto LAB_0803a85e;
    }
    if ((int)uVar5 <= (int)DAT_0803a594) {
      if (uVar5 == DAT_0803a594 - 0x85) {
        FUN_0801abf0(1 - ((byte)*param_1 & 1),DAT_0803a688);
        goto LAB_0803a85e;
      }
      if ((int)uVar5 <= (int)(DAT_0803a594 - 0x85)) {
        if (uVar5 == DAT_0803a594 - 0x144) {
          uVar3 = (uint)(byte)*param_1;
          iVar6 = (1 - (uVar3 & 1)) * DAT_0803a514 + DAT_0803a510;
          if ((*(byte *)(iVar6 + 0x1c) & 0x3f) != 0 || *(char *)(iVar6 + 0x1b) < '\0') {
            iVar6 = (1 - (uVar3 & 1)) * DAT_0803a514 + DAT_0803a510;
            FUN_0801abf0(1 - (uVar3 & 1),
                         ((*(byte *)(iVar6 + 0x1c) & 0x3f) << 1 |
                         (uint)(*(byte *)(iVar6 + 0x1b) >> 7)) * 400);
          }
        }
        else if (uVar5 == DAT_0803a594 - 0x9c) {
          FUN_0801abf0(1 - ((byte)*param_1 & 1),DAT_0803a670);
        }
        goto LAB_0803a85e;
      }
      if ((uVar5 != DAT_0803a5a8) && (uVar5 != DAT_0803a5a8 + 0x54)) goto LAB_0803a85e;
      goto LAB_0803a652;
    }
    if (uVar5 == DAT_0803a5c8) goto LAB_0803a61e;
    if ((int)uVar5 <= (int)DAT_0803a5c8) {
      if (uVar5 != DAT_0803a5cc) {
        if ((uVar5 != DAT_0803a5cc + 0x94) ||
           (uVar3 = (uint)(byte)*param_1,
           (*(uint *)((1 - (uVar3 & 1)) * DAT_0803a514 + DAT_0803a510 + 0x1c) & 0xfffff) >> 0xd == 0
           )) goto LAB_0803a85e;
        uVar5 = (*(uint *)((1 - (uVar3 & 1)) * DAT_0803a514 + DAT_0803a510 + 0x1c) & 0xfffff) >> 0xd
        ;
        iVar6 = 100;
        goto LAB_0803a7ae;
      }
      goto LAB_0803a652;
    }
    if (uVar5 == DAT_0803a5e4) {
      uVar2 = *param_1;
      uVar4 = FUN_080122ec((uVar3 & 0x1ff) >> 1);
      FUN_0801abf0(-((int)((uint)(byte)uVar2 << 0x1f) >> 0x1f),uVar4);
      goto LAB_0803a85e;
    }
    if ((int)DAT_0803a5e4 < (int)uVar5) {
      if (uVar5 == DAT_0803a5f4) {
        iVar7 = 0;
        iVar6 = 0;
        uVar3 = (uint)(byte)*param_1;
        if ((*(uint *)(-((int)(uVar3 << 0x1f) >> 0x1f) * DAT_0803a514 + DAT_0803a510 + 0x1c) &
            0xfffff) >> 0xd != 0) {
          do {
            iVar1 = (int)(uVar3 << 0x1f) >> 0x1f;
            if ((*(byte *)((*(byte *)(iVar6 + DAT_0803a514 * -iVar1 + DAT_0803a86c + DAT_0803a510) &
                           0x7f) * 0x50 +
                           DAT_0803a514 *
                           -((int)((*(byte *)(iVar6 + DAT_0803a514 * -iVar1 +
                                             DAT_0803a86c + DAT_0803a510) & 0x80) << 0x18) >> 0x1f)
                           + DAT_0803a510 + 0x30) & 0x1f) == 0x16) {
              iVar7 = iVar7 + 1;
            }
            iVar6 = iVar6 + 1;
          } while (iVar6 < (int)((*(uint *)(DAT_0803a514 * -iVar1 + DAT_0803a510 + 0x1c) & 0xfffff)
                                >> 0xd));
        }
        if (0 < iVar7) {
          FUN_0801abf0(1 - (uVar3 & 1),iVar7 * 200);
        }
      }
      goto LAB_0803a85e;
    }
    if (uVar5 != DAT_0803a5e4 - 0x3d) goto LAB_0803a85e;
    uVar3 = (byte)*param_1 & 1;
  }
  else {
    if (uVar5 != DAT_0803a51c) {
      if ((int)uVar5 <= (int)DAT_0803a51c) {
        if (uVar5 == DAT_0803a51c - 0xbd) {
          FUN_0801abf0(1 - ((byte)*param_1 & 1),600);
          goto LAB_0803a85e;
        }
        if ((int)uVar5 <= (int)(DAT_0803a51c - 0xbd)) {
          if (uVar5 == DAT_0803a51c - 0xbf) {
            FUN_0801abf0(1 - ((byte)*param_1 & 1),200);
            goto LAB_0803a85e;
          }
          uVar3 = DAT_0803a51c - 0xbe;
          goto LAB_0803a566;
        }
        if (uVar5 == 0x1100) goto LAB_0803a63e;
        if (uVar5 != 0x1101) goto LAB_0803a85e;
        FUN_0801abf0(1 - ((byte)*param_1 & 1),1000);
        uVar3 = (byte)*param_1 & 1;
        goto LAB_0803a6a4;
      }
      if ((int)uVar5 <= DAT_0803a554) {
        if ((int)uVar5 < DAT_0803a554 + -1) {
          if (uVar5 == DAT_0803a558) {
            FUN_0801abf0(1 - ((byte)*param_1 & 1),300);
            goto LAB_0803a85e;
          }
          if ((uVar5 != DAT_0803a558 + 0x1e) ||
             (uVar3 = (uint)(byte)*param_1, iVar6 = (1 - (uVar3 & 1)) * DAT_0803a514 + DAT_0803a510,
             (*(byte *)(iVar6 + 0x1c) & 0x3f) == 0 && -1 < *(char *)(iVar6 + 0x1b)))
          goto LAB_0803a85e;
          iVar6 = (1 - (uVar3 & 1)) * DAT_0803a514 + DAT_0803a510;
          uVar5 = (*(byte *)(iVar6 + 0x1c) & 0x3f) << 1 | (uint)(*(byte *)(iVar6 + 0x1b) >> 7);
          iVar6 = 200;
LAB_0803a7ae:
          FUN_0801abf0(1 - (uVar3 & 1),iVar6 * uVar5);
          goto LAB_0803a85e;
        }
LAB_0803a63e:
        FUN_0801abf0(1 - ((byte)*param_1 & 1),800);
        goto LAB_0803a85e;
      }
      if (uVar5 != 0x1460) {
        uVar3 = 0x1525;
LAB_0803a566:
        if (uVar5 != uVar3) goto LAB_0803a85e;
        goto LAB_0803a61e;
      }
    }
LAB_0803a652:
    uVar3 = 1 - ((byte)*param_1 & 1);
  }
  FUN_0801abf0(uVar3,1000);
LAB_0803a85e:
  return (ulonglong)in_lr << 0x20;
}



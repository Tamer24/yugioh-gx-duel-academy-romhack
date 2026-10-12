// ===== 0803A20C FUN_0803a20c

longlong FUN_0803a20c(ushort *param_1)

{
  byte bVar1;
  byte bVar2;
  int iVar4;
  undefined4 uVar5;
  undefined2 uVar6;
  uint uVar7;
  int iVar8;
  int *piVar9;
  uint in_lr;
  char acStack_2c [4];
  int aiStack_28 [2];
  byte bVar3;
  
  if ((param_1[1] & 8) != 0) goto LAB_0803a47a;
  uVar7 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                     SUB_0803a288 * ((*param_1 & 0x1ff) >> 8) + DAT_0803a284 + 0x24) & 0x7fff) * 2 +
                 DAT_0803a280);
  if (uVar7 == DAT_0803a28c) {
    uVar7 = (byte)*param_1 & 1;
    uVar6 = 400;
  }
  else if ((int)DAT_0803a28c < (int)uVar7) {
    if (uVar7 == DAT_0803a2cc) {
      uVar7 = (byte)*param_1 & 1;
      uVar6 = 2000;
    }
    else if ((int)DAT_0803a2cc < (int)uVar7) {
      if (uVar7 == DAT_0803a2f4) {
        uVar7 = 1 - ((byte)*param_1 & 1);
        goto LAB_0803a354;
      }
      if ((int)DAT_0803a2f4 < (int)uVar7) {
        if (uVar7 != DAT_0803a304) goto LAB_0803a47a;
        bVar3 = (byte)*param_1;
        bVar2 = (byte)param_1[(byte)param_1[5] + 6];
        bVar1 = *(byte *)((int)param_1 + ((byte)param_1[5] + 1) * 2 + 9);
      }
      else {
        if (uVar7 != DAT_0803a2f4 - 0x55) goto LAB_0803a47a;
        bVar3 = (byte)*param_1;
        bVar2 = (byte)param_1[5];
        bVar1 = *(byte *)((int)param_1 + 9);
      }
      uVar7 = bVar3 & 1;
      uVar6 = CONCAT11(bVar2,bVar1);
    }
    else {
      if (uVar7 != DAT_0803a2cc - 0x9f) {
        if ((int)uVar7 <= (int)(DAT_0803a2cc - 0x9f)) {
          if (uVar7 == DAT_0803a2cc - 0xd4) {
            iVar8 = 0;
            do {
              if (iVar8 == 0) {
                uVar7 = (byte)*param_1 & 1;
              }
              else {
                uVar7 = 1 - ((byte)*param_1 & 1);
              }
              iVar4 = FUN_08010a30(DAT_0803a3dc,0xff,1 << (uVar7 & 0xff) & 0xffff,1,0xe,0,
                                   acStack_2c + uVar7);
              aiStack_28[uVar7] = iVar4;
              uVar5 = 0x29;
              if (uVar7 != 0) {
                uVar5 = DAT_0803a3e0;
              }
              drawing_FUN_08022034(uVar5,1000,0);
              iVar8 = iVar8 + 1;
            } while (iVar8 < 2);
            iVar8 = 0;
            do {
              if (iVar8 == 0) {
                uVar7 = (byte)*param_1 & 1;
              }
              else {
                uVar7 = 1 - ((byte)*param_1 & 1);
              }
              piVar9 = aiStack_28 + uVar7;
              iVar8 = iVar8 + 1;
              if ((0 < *piVar9) && (acStack_2c[uVar7] != -1)) {
                FUN_0801aaa4(uVar7,acStack_2c[uVar7]);
                iVar4 = 0;
                if (0 < *piVar9) {
                  do {
                    FUN_0801abf0(1 - uVar7,500);
                    iVar4 = iVar4 + 1;
                  } while (iVar4 < *piVar9);
                }
              }
            } while (iVar8 < 2);
          }
          goto LAB_0803a47a;
        }
        if (uVar7 != DAT_0803a2d8) goto LAB_0803a47a;
        goto LAB_0803a308;
      }
LAB_0803a33e:
      uVar7 = (byte)*param_1 & 1;
      uVar6 = 800;
    }
  }
  else if (uVar7 == DAT_0803a290) {
    uVar7 = (byte)*param_1 & 1;
    uVar6 = 600;
  }
  else if ((int)DAT_0803a290 < (int)uVar7) {
    if (uVar7 != DAT_0803a2a8) {
      if ((int)uVar7 < (int)DAT_0803a2a8) goto LAB_0803a33e;
      if (uVar7 != DAT_0803a2ac) goto LAB_0803a47a;
    }
    uVar7 = (byte)*param_1 & 1;
LAB_0803a354:
    uVar6 = 1000;
  }
  else if (uVar7 == DAT_0803a290 - 2) {
LAB_0803a308:
    uVar7 = (byte)*param_1 & 1;
    uVar6 = 200;
  }
  else {
    if (((int)uVar7 <= (int)(DAT_0803a290 - 2)) && (uVar7 != DAT_0803a290 - 0xae))
    goto LAB_0803a47a;
    uVar7 = (byte)*param_1 & 1;
    uVar6 = 500;
  }
  FUN_0801ad6c(uVar7,uVar6);
LAB_0803a47a:
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


// ===== 0803DFE4 FUN_0803dfe4

undefined8 FUN_0803dfe4(byte *param_1)

{
  byte bVar1;
  byte bVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 in_lr;
  
  bVar1 = param_1[2];
  if ((bVar1 & 8) == 0) {
    bVar2 = *(byte *)(DAT_0803e010 + DAT_0803e014);
    if (bVar2 == 0x7f) {
      iVar3 = show_confirmation_prompt(DAT_0803e068,0xff,3,1,6,1);
      if (iVar3 != 0) {
        if ((*param_1 & 1) == 0) {
          ask_yes_or_no_question(DAT_0803e09c);
        }
        else if ((*(ushort *)(DAT_0803e06c + DAT_0803e070) & 0x1fff) >> 6 < 4) {
          *(ushort *)(DAT_0803e088 + DAT_0803e08c) = bVar1 & 8;
        }
        else {
          *(undefined2 *)(DAT_0803e074 + DAT_0803e078) = 1;
        }
        uVar4 = 0x7e;
        goto LAB_0803e0ba;
      }
    }
    else if (bVar2 < 0x80) {
      if ((bVar2 == 0x7e) && (*(short *)(DAT_0803e0c4 + DAT_0803e0c8) != 0)) {
        FUN_0801b28c(*param_1 & 1,1);
      }
    }
    else if (bVar2 == 0x80) {
      FUN_0801b28c(*param_1 & 1,2);
      uVar4 = 0x7f;
      goto LAB_0803e0ba;
    }
  }
  uVar4 = 0;
LAB_0803e0ba:
  return CONCAT44(in_lr,uVar4);
}



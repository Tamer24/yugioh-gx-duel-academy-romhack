// ===== 0803B7D0 FUN_0803b7d0

longlong FUN_0803b7d0(uint *param_1)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  uint in_lr;
  
  if ((*param_1 & 0x7e000) == 0x20000) {
    bVar1 = (byte)param_1[1];
    uVar2 = (ushort)param_1[1] >> 8;
    iVar3 = FUN_0800e874(bVar1,uVar2);
    if (((iVar3 != 0) && (iVar3 = FUN_0800e8d0(bVar1,uVar2), iVar3 == 0)) &&
       (((byte)*param_1 & 1) != bVar1)) {
      FUN_0801a36c(bVar1,uVar2,0,0);
    }
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 08031DD0 FUN_08031dd0

undefined8 FUN_08031dd0(uint *param_1)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 in_lr;
  
  if ((*param_1 & 0x7e000) == 0x20000) {
    bVar1 = (byte)param_1[1];
    uVar2 = (ushort)param_1[1] >> 8;
    iVar3 = FUN_0800e874(bVar1,uVar2);
    if (((iVar3 == 0) || (iVar3 = FUN_0800e8d0(bVar1,uVar2), iVar3 != 0)) ||
       (((byte)*param_1 & 1) == bVar1)) goto LAB_08031e0c;
  }
  else {
LAB_08031e0c:
    iVar3 = FUN_08010c10((byte)*param_1 & 1,1,0);
    if (iVar3 < 1) {
      uVar4 = 0;
      goto LAB_08031e24;
    }
  }
  uVar4 = 1;
LAB_08031e24:
  return CONCAT44(in_lr,uVar4);
}


// ===== 08052E7C FUN_08052e7c

undefined8 FUN_08052e7c(byte *param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  undefined4 in_lr;
  
  uVar3 = *(uint *)(DAT_08052ecc + 0x7c0);
  if ((uVar3 & 0x3ffff) >> 10 == 0) {
    param_1[8] = param_1[8] & 0xf0;
    iVar1 = FUN_08010c10(*param_1 & 1,1,0);
    if (iVar1 != 0) {
                    /* WARNING: Subroutine does not return */
      ask_question(DAT_08052ed0);
    }
LAB_08052f18:
    uVar2 = 1;
  }
  else {
    if ((*(ushort *)(DAT_08052ef4 + 0x148) & 2) == 0) {
      iVar1 = FUN_08009094(0xe0);
      if ((iVar1 != 0) &&
         (iVar1 = FUN_08051680(param_1,*(undefined1 *)(DAT_08052f1c + DAT_08052f20)), iVar1 != 0))
      goto LAB_08052f18;
    }
    else {
      *(uint *)(DAT_08052ecc + 0x7c0) = uVar3 & DAT_08052ef8;
    }
    uVar2 = 0;
  }
  return CONCAT44(in_lr,uVar2);
}


// ===== 0803991C card_effect_handler_common_33cards

longlong card_effect_handler_common_33cards(ushort *param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  undefined4 uVar4;
  uint in_lr;
  
  uVar2 = (uint)*param_1;
  if ((((((*(uint *)(((uVar2 & 0x1ff) >> 1 & 0x7f) * 0x50 + DAT_08039a04 * ((uVar2 & 0x1ff) >> 8) +
                     DAT_08039a00 + 0x30) & 0xfffff) >> 0xc & 0x7f) != 5) ||
       (-1 < (int)((uint)*(byte *)(((uVar2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                   DAT_08039a04 * ((uVar2 & 0x1ff) >> 8) + DAT_08039a00 + 0x33) *
                  0x8000000))) || ((param_1[4] & 0xf) == 0)) ||
     ((iVar3 = (*(byte *)((int)param_1 + 9) & 0x7f) * 0x50 +
               DAT_08039a04 * -((int)((*(byte *)((int)param_1 + 9) & 0x80) << 0x18) >> 0x1f) +
               DAT_08039a00, ((*(uint *)(iVar3 + 0x30) & 0xfffff) >> 0xc & 0x7f) != 0 ||
      (-1 < (int)((uint)*(byte *)(iVar3 + 0x33) * 0x8000000))))) goto LAB_08039a74;
  uVar2 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((uVar2 & 0x1ff) >> 1 & 0x7f) * 0x50 + DAT_08039a04 * ((uVar2 & 0x1ff) >> 8) +
                     DAT_08039a00 + 0x24) & 0x7fff) * 2 + DAT_08039a08);
  if (uVar2 == DAT_08039a0c) {
LAB_08039a48:
    uVar4 = 0x42;
    if ((*param_1 & 1) != 0) {
      uVar4 = DAT_08039a80;
    }
    drawing_FUN_08022084(uVar4,(*param_1 & 0x1ff) >> 1);
  }
  else {
    if ((int)DAT_08039a0c < (int)uVar2) {
      uVar1 = DAT_08039a40;
      if (uVar2 == DAT_08039a3c) goto LAB_08039a48;
    }
    else {
      uVar1 = DAT_08039a0c - 0x47;
    }
    if (uVar2 == uVar1) {
      uVar4 = 0x3d;
      if ((*param_1 & 1) != 0) {
        uVar4 = DAT_08039a44;
      }
      drawing_FUN_08022034(uVar4,(*param_1 & 0x1ff) >> 1,(byte)param_1[5]);
    }
  }
  FUN_0801a600((byte)*param_1 & 1,(*param_1 & 0x1ff) >> 1,*(byte *)((int)param_1 + 9));
LAB_08039a74:
  return (ulonglong)in_lr << 0x20;
}


// ===== 080296D0 FUN_080296d0

void FUN_080296d0(ushort *param_1,uint param_2)

{
  ushort uVar1;
  int iVar2;
  byte bVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  int iVar7;
  int extraout_r1;
  uint extraout_r1_00;
  undefined4 uVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  int iVar12;
  uint uVar13;
  code *UNRECOVERED_JUMPTABLE;
  ulonglong uVar14;
  
  iVar7 = iRam080297c4;
  uVar1 = *(ushort *)
           (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 + ((*param_1 & 0x1ff) >> 8) * iRam080297c4 +
            iRam080297c8 + 0x24);
  uVar10 = param_2 & 0x7f;
  iVar4 = uVar10 * 0x50;
  uVar5 = param_2 & 0x80;
  iVar6 = (uVar5 >> 7) * iRam080297c4 + iVar4;
  iVar12 = iVar6 + iRam080297c8;
  uVar13 = *(ushort *)(iVar12 + 0x24) & 0x7fff;
  uVar11 = *(uint *)(iVar12 + 0x30) & 0xfffff;
  uVar9 = uVar11 >> 0x13;
  if ((uVar11 >> 0xc & 0x7f) != 0) {
    FUN_08029f70();
  }
  if (-1 < (int)((uint)*(byte *)(iVar12 + 0x33) * 0x8000000)) {
    FUN_08029f70();
  }
  iVar2 = iRam080297cc;
  uVar1 = *(ushort *)((uVar1 & 0x7fff) * 2 + iRam080297cc);
  uVar14 = (ulonglong)CONCAT24(uVar1,uRam080297d0);
  if (uVar1 == uRam080297d0) {
    uVar14 = FUN_08029f68();
  }
  uVar11 = (uint)(uVar14 >> 0x20);
  if ((int)uVar14 < (int)uVar11) {
    if (uVar11 == DAT_08029928) {
LAB_08029a88:
      uVar11 = 0;
      if ((*(byte *)((param_2 & 0x7f) * 0x50 + DAT_08029ab8 * ((param_2 & 0x80) >> 7) + DAT_08029abc
                    + 0x30) & 0x1f) != 0xf) goto LAB_08029f72;
      goto LAB_08029c76;
    }
    if ((int)DAT_08029928 < (int)uVar11) {
      if ((int)uVar11 <= DAT_080299e0) {
        if (((int)uVar11 < DAT_080299e0 + -5) && (uVar11 != DAT_080299e4)) {
          if ((int)DAT_080299e4 < (int)uVar11) {
            if (uVar11 == DAT_08029a0c) {
              if (1 < (*(byte *)(iVar12 + 0x31) & 0xf)) goto code_r0x08029f68;
            }
            else if ((int)DAT_08029a0c < (int)uVar11) {
              if (uVar11 != DAT_08029a1c) {
                uVar5 = DAT_08029a1c + 0x3f;
                goto LAB_08029a3a;
              }
            }
            else if (uVar11 == DAT_08029a0c - 0x45) {
              uVar11 = (uint)(*(uint *)(iVar6 + DAT_08029f4c + 0x28) < 0x3e9);
              goto LAB_08029f72;
            }
            goto code_r0x08029f70;
          }
          if (uVar11 != DAT_080299e4 - 3) {
            uVar5 = DAT_080299f0;
            if ((int)(DAT_080299e4 - 3) < (int)uVar11) goto LAB_080299ea;
            if (uVar11 != DAT_080299e4 - 0x20) goto code_r0x08029f70;
            goto LAB_08029b36;
          }
        }
code_r0x08029f68:
        uVar11 = 1;
        goto LAB_08029f72;
      }
      if (uVar11 == DAT_08029a44) {
        if ((0x1a < (uVar10 - 100 & 0xffff)) && (iVar7 = FUN_080dd52c(uVar13), iVar7 != 0)) {
LAB_08029e86:
          if ((*(byte *)(iVar12 + 0x31) & 0xf) < 7) goto code_r0x08029f68;
        }
      }
      else if ((int)DAT_08029a44 < (int)uVar11) {
        if (DAT_08029a74 < (int)uVar11) {
          if (((uVar11 == DAT_08029a84) && (0x1a < (uVar10 - 100 & 0xffff))) &&
             (uVar9 == ((byte)*param_1 & 1))) {
            uVar11 = (uint)*(ushort *)(uVar13 * 2 + iVar2);
            if (uVar11 == DAT_08029ef4) goto code_r0x08029f68;
            if (((int)DAT_08029ef4 <= (int)uVar11) && ((int)uVar11 <= (int)(DAT_08029ef4 + 0x5f))) {
              iVar7 = DAT_08029ef4 + 0x5e;
              goto LAB_08029d9e;
            }
          }
        }
        else if ((((int)uVar11 < DAT_08029a74 + -1) && (uVar11 == DAT_08029a74 - 0x86U)) &&
                ((0x1a < (uVar10 - 100 & 0xffff) && (iVar6 = FUN_080dd55c(uVar13), iVar6 != 0)))) {
          iVar12 = (uVar5 >> 7) * iVar7 + iVar4 + DAT_08029ebc;
          goto LAB_08029e86;
        }
      }
      else if (uVar11 == DAT_08029a48) {
        if (0x1a < (uVar10 - 100 & 0xffff)) {
          uVar11 = (uint)*(ushort *)(uVar13 * 2 + iVar2);
          if (DAT_08029e48 < (int)uVar11) {
            if (uVar11 != DAT_08029e60) {
              uVar5 = DAT_08029e68;
              if ((int)uVar11 <= (int)DAT_08029e60) {
                uVar5 = DAT_08029e60 - 0x8b;
              }
              goto LAB_08029a3a;
            }
          }
          else {
            uVar5 = DAT_08029e4c;
            if ((int)uVar11 < DAT_08029e48 + -1) goto LAB_08029a3a;
          }
          goto code_r0x08029f68;
        }
      }
      else {
        if ((int)uVar11 <= (int)DAT_08029a48) {
          uVar5 = DAT_08029a48 - 0x69;
          goto LAB_08029a3a;
        }
        if (((uVar11 == DAT_08029a58) &&
            (bVar3 = *(byte *)((uVar5 >> 7) * iVar7 + iVar4 + DAT_08029cfc + 0x30) & 0x1f,
            bVar3 < 0xd)) && (10 < bVar3)) goto code_r0x08029f68;
      }
    }
    else if ((int)(DAT_08029928 - 0xab) < (int)uVar11) {
      if (DAT_08029978 < (int)uVar11) {
        if (uVar11 == DAT_080299a4) {
          if (0x1a < (uVar10 - 100 & 0xffff)) {
            iVar7 = uVar13 << 1;
            uVar11 = DAT_08029e1c;
LAB_08029dc0:
            if (*(ushort *)(iVar7 + iVar2) == uVar11) goto code_r0x08029f68;
          }
        }
        else {
          uVar5 = DAT_080299ac;
          if ((int)uVar11 <= (int)DAT_080299a4) {
            if ((uVar11 != DAT_080299a4 - 0x2f) || ((uVar10 - 100 & 0xffff) < 0x1b))
            goto code_r0x08029f70;
            uVar11 = (uint)*(ushort *)(uVar13 * 2 + iVar2);
            if (uVar11 == DAT_08029df4) goto code_r0x08029f68;
            uVar5 = DAT_08029e00;
            if ((int)uVar11 <= (int)DAT_08029df4) {
              uVar5 = DAT_08029df8;
            }
          }
LAB_08029a3a:
          if (uVar11 == uVar5) goto code_r0x08029f68;
        }
      }
      else {
        if ((DAT_08029978 + -2 <= (int)uVar11) || (uVar11 == DAT_08029978 - 0x55U))
        goto code_r0x08029f68;
        if ((int)(DAT_08029978 - 0x55U) < (int)uVar11) {
          if ((uVar11 == DAT_08029988) && ((*(byte *)(iVar12 + 0x30) & 0x1f) == 7)) {
            bVar3 = (byte)*param_1;
LAB_08029d4c:
            if (-((int)((uint)bVar3 << 0x1f) >> 0x1f) == uVar9) goto code_r0x08029f68;
          }
        }
        else {
          uVar5 = DAT_08029978 - 0x67;
LAB_080299ea:
          if (uVar11 == uVar5) goto LAB_08029a88;
        }
      }
    }
    else {
      if (((int)(DAT_08029928 - 0xac) <= (int)uVar11) || (uVar11 == DAT_08029928 - 0x185))
      goto code_r0x08029f68;
      if ((int)(DAT_08029928 - 0x185) < (int)uVar11) {
        if (uVar11 != DAT_08029944) {
          if ((int)DAT_08029944 < (int)uVar11) {
            if (uVar11 != DAT_08029954) {
              uVar5 = DAT_08029954 + 0x58;
              goto LAB_08029a3a;
            }
            goto LAB_08029a88;
          }
          if (((uVar11 == DAT_08029944 - 0x44) && (((byte)*param_1 & 1) != uVar9)) &&
             (*(ushort *)(uVar13 * 2 + iVar2) != DAT_08029f6c)) goto code_r0x08029f68;
        }
      }
      else if ((int)(DAT_08029928 - 0x192) <= (int)uVar11) {
        if ((int)uVar11 <= (int)(DAT_08029928 - 0x191)) {
          uVar11 = -(*(byte *)(iVar12 + 0x30) & 0x1f ^ 7) >> 0x1f;
          goto LAB_08029f72;
        }
        uVar5 = DAT_08029928 - 0x187;
LAB_08029920:
        if (uVar11 == uVar5) {
          uVar11 = 0;
          if (((byte)*param_1 & 1) != uVar9) goto LAB_08029f72;
          goto LAB_08029f06;
        }
      }
    }
  }
  else {
    if (uVar11 != uRam080297d4) {
      if ((int)uRam080297d4 < (int)uVar11) {
        if (uVar11 == DAT_08029858) {
          uVar11 = 0;
          if ((*(byte *)(iVar12 + 0x30) & 0x1f) != 0xe) goto LAB_08029f72;
        }
        else {
          if ((int)DAT_08029858 < (int)uVar11) {
            if (DAT_080298a0 < (int)uVar11) {
              if (uVar11 == DAT_080298cc) {
LAB_08029ae8:
                uVar11 = 0;
                if ((*(byte *)((param_2 & 0x7f) * 0x50 + DAT_08029b18 * ((param_2 & 0x80) >> 7) +
                               DAT_08029b1c + 0x30) & 0x1f) != 7) goto LAB_08029f72;
                goto LAB_08029c76;
              }
              if ((int)DAT_080298cc < (int)uVar11) {
                if (uVar11 == DAT_080298e4) {
LAB_08029d06:
                  uVar8 = 4;
                  goto LAB_08029d1c;
                }
                if (uVar11 == DAT_080298e4 + 1) {
                  uVar8 = 6;
                  goto LAB_08029d1c;
                }
              }
              else if (uVar11 == DAT_080298cc - 0x84) goto LAB_08029d0c;
            }
            else {
              if (DAT_080298a0 + -1 <= (int)uVar11) goto code_r0x08029f68;
              if (uVar11 == DAT_080298a0 - 6U) {
                if (0x1a < (uVar10 - 100 & 0xffff)) {
                  iVar7 = uVar13 * 2;
                  uVar11 = DAT_08029dcc;
                  goto LAB_08029dc0;
                }
              }
              else {
                if ((int)uVar11 <= (int)(DAT_080298a0 - 6U)) {
                  uVar5 = DAT_080298a0 - 7;
                  goto LAB_08029920;
                }
                if (uVar11 == DAT_080298b0) goto LAB_08029d06;
              }
            }
            goto code_r0x08029f70;
          }
          if (uVar11 != DAT_08029858 - 5) {
            if ((int)(DAT_08029858 - 5) < (int)uVar11) {
              if (uVar11 == DAT_0802987c) goto LAB_08029ae8;
              if ((int)uVar11 < (int)DAT_0802987c) {
                uVar8 = 5;
                goto LAB_08029d1c;
              }
              if (uVar11 == DAT_0802987c + 1) {
                uVar11 = 0;
                if ((*(byte *)((param_2 & 0x7f) * 0x50 + DAT_08029b98 * ((param_2 & 0x80) >> 7) +
                               DAT_08029b9c + 0x30) & 0x1f) != 9) goto LAB_08029f72;
              }
              else {
                if (uVar11 != DAT_0802987c + 2) goto code_r0x08029f70;
                uVar11 = 0;
                if ((*(byte *)((param_2 & 0x7f) * 0x50 + DAT_08029c30 * ((param_2 & 0x80) >> 7) +
                               DAT_08029c34 + 0x30) & 0x1f) != 0x10) goto LAB_08029f72;
              }
            }
            else {
              if (uVar11 == DAT_08029858 - 7) goto code_r0x08029f68;
              if ((int)(DAT_08029858 - 7) < (int)uVar11) {
                uVar11 = 0;
                if ((*(byte *)((uVar5 >> 7) * iVar7 + iVar4 + DAT_08029ca8 + 0x30) & 0x1f) != 2)
                goto LAB_08029f72;
                goto LAB_08029f06;
              }
              if (uVar11 != DAT_08029858 - 9) goto code_r0x08029f70;
              uVar11 = 0;
              if ((*(byte *)((param_2 & 0x7f) * 0x50 + DAT_08029c7c * ((param_2 & 0x80) >> 7) +
                             DAT_08029c80 + 0x30) & 0x1f) != 0xc) goto LAB_08029f72;
            }
            goto LAB_08029c76;
          }
          uVar11 = 0;
          if ((*(byte *)(iVar12 + 0x30) & 0x1f) != 0x12) goto LAB_08029f72;
        }
      }
      else if (uVar11 == uRam080297d4 - 9) {
        uVar11 = 0;
        if ((*(byte *)(iVar12 + 0x30) & 0x1f) != 0xb) goto LAB_08029f72;
      }
      else if ((int)(uRam080297d4 - 9) < (int)uVar11) {
LAB_080297f0:
        if (uVar11 == DAT_08029810) {
LAB_08029b36:
          uVar11 = 0;
          if ((*(byte *)((param_2 & 0x7f) * 0x50 + DAT_08029b64 * ((param_2 & 0x80) >> 7) +
                         DAT_08029b68 + 0x30) & 0x1f) != 0x11) goto LAB_08029f72;
LAB_08029c76:
          uVar11 = 1;
          goto LAB_08029f72;
        }
        if ((int)DAT_08029810 < (int)uVar11) {
          if (uVar11 == DAT_08029824) {
            uVar11 = 0;
            if ((*(byte *)(iVar12 + 0x30) & 0x1f) != 1) goto LAB_08029f72;
          }
          else {
            if ((int)uVar11 <= (int)DAT_08029824) goto code_r0x08029f68;
            uVar11 = 0;
            if ((*(byte *)((uVar5 >> 7) * iVar7 + iVar4 + DAT_08029bd8 + 0x30) & 0x1f) != 0x13)
            goto LAB_08029f72;
          }
        }
        else {
          if (uVar11 != DAT_08029810 - 2) {
            if ((int)uVar11 <= (int)(DAT_08029810 - 2)) {
              uVar8 = 3;
              goto LAB_08029d1c;
            }
            goto code_r0x08029f68;
          }
          uVar11 = 0;
          if ((*(byte *)(iVar12 + 0x30) & 0x1f) != 0xd) goto LAB_08029f72;
        }
      }
      else if (uVar11 == uRam080297d4 - 0xe) {
        uVar11 = 0;
        if ((*(byte *)(iVar12 + 0x30) & 0x1f) != 3) goto LAB_08029f72;
      }
      else {
        if ((int)uVar11 <= (int)(uRam080297d4 - 0xe)) {
          if (uVar11 == uRam080297d4 - 0x10) goto LAB_08029a88;
          if ((int)(uRam080297d4 - 0x10) < (int)uVar11) {
            uVar8 = 2;
            goto LAB_08029d1c;
          }
          if (uVar11 == uRam080297d4 - 0xf5) {
            if ((0x1a < ((param_2 & 0x7f) - 100 & 0xffff)) &&
               (*(ushort *)(uVar13 * 2 + DAT_08029d58) == DAT_08029d5c)) {
              bVar3 = (byte)*param_1;
              goto LAB_08029d4c;
            }
            goto code_r0x08029f70;
          }
          FUN_08029f70();
          *(short *)(iVar2 + 0x30) = (short)iVar2;
          uVar11 = extraout_r1 >> 0xc;
        }
        if (iRam080297ec < (int)uVar11) {
LAB_08029d0c:
          uVar8 = 1;
LAB_08029d1c:
          uVar11 = FUN_0800ddc0(param_2 & 0xffff,uVar8);
          uVar11 = uVar11 & 0xffff;
          goto LAB_08029f72;
        }
        if ((int)uVar11 < iRam080297ec + -1) {
          FUN_08029f68();
          uVar11 = extraout_r1_00;
          goto LAB_080297f0;
        }
        uVar11 = 0;
        if ((*(byte *)((uVar5 >> 7) * iVar7 + iVar4 + DAT_08029ae4 + 0x30) & 0x1f) != 10)
        goto LAB_08029f72;
      }
LAB_08029f06:
      uVar11 = 1;
      goto LAB_08029f72;
    }
    if ((uVar10 - 100 & 0xffff) < 0x1b) goto code_r0x08029f70;
    uVar11 = (uint)*(ushort *)(uVar13 * 2 + iVar2);
    if (uVar11 == DAT_08029d8c) goto code_r0x08029f68;
    if ((int)DAT_08029d8c < (int)uVar11) {
      if ((int)uVar11 <= DAT_08029da8) {
        iVar7 = DAT_08029da8 + -2;
        goto LAB_08029d9e;
      }
    }
    else if ((int)uVar11 <= DAT_08029d90) {
      iVar7 = DAT_08029d90 + -1;
LAB_08029d9e:
      if (iVar7 <= (int)uVar11) goto code_r0x08029f68;
    }
  }
code_r0x08029f70:
  uVar11 = 0;
LAB_08029f72:
                    /* WARNING: Could not recover jumptable at 0x08029f80. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(uVar11);
  return;
}


// ===== 08051F10 FUN_08051f10

undefined8 FUN_08051f10(byte *param_1)

{
  char cVar1;
  undefined1 uVar2;
  short sVar3;
  uint uVar4;
  undefined4 uVar5;
  int iVar6;
  int unaff_r4;
  int iVar7;
  int iVar8;
  ushort *puVar9;
  undefined4 in_lr;
  undefined8 uVar10;
  
  uVar4 = ((param_1[1] & 0x1f) >> 1) - 1;
  if (uVar4 < 6) {
                    /* WARNING: Could not recover jumptable at 0x08051f2c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    uVar10 = (**(code **)(uVar4 * 4 + DAT_08051f30))();
    return uVar10;
  }
  if ((*param_1 & 1) == 0) {
    uVar4 = *(uint *)(DAT_080520c4 + 0x7c0);
    if ((uVar4 & 0x3ffff) >> 10 == 0) {
                    /* WARNING: Subroutine does not return */
      ask_question(DAT_080520c8);
    }
    if ((*(ushort *)(DAT_080520ec + 0x148) & 2) == 0) {
      iVar8 = FUN_08009094(DAT_08052134);
      if (iVar8 != 0) {
        uVar2 = *(undefined1 *)(DAT_08052138 + DAT_0805213c);
        sVar3 = FUN_080616b8(param_1,uVar2);
        if ((sVar3 != 0) && (iVar8 = FUN_08051680(param_1,uVar2), iVar8 != 0)) goto LAB_08051f8a;
        FUN_080e6d88(3);
      }
    }
    else {
      *(uint *)(DAT_080520c4 + 0x7c0) = uVar4 & DAT_080520f0;
    }
    uVar5 = 0;
  }
  else {
    param_1[8] = param_1[8] & 0xf0;
    iVar8 = DAT_08052078;
    iVar7 = 0;
    puVar9 = (ushort *)(unaff_r4 * 2 + DAT_0805207c);
    do {
      cVar1 = *(char *)(iVar7 + iVar8);
      if ((((cVar1 != -1) && (iVar6 = FUN_080616b8(param_1,cVar1), iVar6 != 0)) &&
          (*puVar9 == DAT_08052080)) && (iVar6 = FUN_08051680(param_1,cVar1), iVar6 != 0))
      goto LAB_08051f8a;
      iVar6 = DAT_08052078;
      iVar7 = iVar7 + 1;
    } while (iVar7 < 5);
    iVar8 = 0;
    do {
      cVar1 = *(char *)(iVar8 + iVar6);
      if (((cVar1 != -1) && (iVar7 = FUN_080616b8(param_1,cVar1), iVar7 != 0)) &&
         (iVar7 = FUN_08051680(param_1,cVar1), iVar7 != 0)) goto LAB_08051f8a;
      iVar7 = DAT_08052084;
      iVar8 = iVar8 + 1;
    } while (iVar8 < 5);
    iVar8 = 0;
    do {
      cVar1 = *(char *)(iVar8 + iVar7);
      if (((cVar1 != -1) && (iVar6 = FUN_080616b8(param_1,cVar1), iVar6 != 0)) &&
         (iVar6 = FUN_08051680(param_1,cVar1), iVar6 != 0)) break;
      iVar8 = iVar8 + 1;
    } while (iVar8 < 5);
LAB_08051f8a:
    uVar5 = 1;
  }
  return CONCAT44(in_lr,uVar5);
}



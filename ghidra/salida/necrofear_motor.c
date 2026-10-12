// ===== 0801E168 FUN_0801e168

undefined4 FUN_0801e168(void)

{
  ushort *puVar1;
  byte bVar2;
  byte bVar3;
  uint uVar4;
  byte *pbVar5;
  uint uVar6;
  uint *puVar7;
  undefined4 in_lr;
  
  puVar1 = DAT_0801e1a0;
  uVar6 = (uint)(*DAT_0801e1a0 >> 0xf);
  uVar4 = (uint)DAT_0801e1a0[1];
  if (uVar4 == DAT_0801e1a4) {
    pbVar5 = (byte *)(DAT_0801e3a4 * uVar6 + DAT_0801e3a0 + DAT_0801e3a4 + -0x1a);
    bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 5;
    bVar2 = 0xdf;
  }
  else if ((int)DAT_0801e1a4 < (int)uVar4) {
    if (uVar4 == DAT_0801e214) {
      pbVar5 = (byte *)(DAT_0801e438 * uVar6 + DAT_0801e434 + DAT_0801e438 + -0x18);
      *pbVar5 = *pbVar5 & 0x7f | (char)DAT_0801e1a0[2] << 7;
      goto LAB_0801e4ce;
    }
    if ((int)DAT_0801e214 < (int)uVar4) {
      if (uVar4 == DAT_0801e244) {
        pbVar5 = (byte *)(DAT_0801e480 * uVar6 + DAT_0801e47c + DAT_0801e480 + -0x17);
        bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 3;
        bVar2 = 0xf7;
      }
      else if ((int)DAT_0801e244 < (int)uVar4) {
        if (uVar4 != DAT_0801e25c) {
          if (uVar4 == DAT_0801e25c + 0x31) {
            puVar7 = (uint *)(DAT_0801e4e8 * uVar6 + DAT_0801e4e4 + DAT_0801e4e8 + -0x18);
            *puVar7 = *puVar7 & DAT_0801e4ec | (DAT_0801e1a0[2] & 0xf) << 0xd;
          }
          goto LAB_0801e4ce;
        }
        pbVar5 = (byte *)(DAT_0801e4ac * uVar6 + DAT_0801e4a8 + DAT_0801e4ac + -0x17);
        bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 4;
        bVar2 = 0xef;
      }
      else {
        if (uVar4 != DAT_0801e244 - 0x1e) goto LAB_0801e4ce;
        pbVar5 = (byte *)(DAT_0801e45c * uVar6 + DAT_0801e458 + DAT_0801e45c + -0x17);
        bVar3 = (byte)DAT_0801e1a0[2] & 7;
        bVar2 = 0xf8;
      }
    }
    else if (uVar4 == DAT_0801e218) {
      pbVar5 = (byte *)(DAT_0801e3ec * uVar6 + DAT_0801e3e8 + DAT_0801e3ec + -0x18);
      bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 1;
      bVar2 = 0xfd;
    }
    else if ((int)DAT_0801e218 < (int)uVar4) {
      if (uVar4 != DAT_0801e228) goto LAB_0801e4ce;
      pbVar5 = (byte *)(DAT_0801e410 * uVar6 + DAT_0801e40c + DAT_0801e410 + -0x18);
      bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 6;
      bVar2 = 0xbf;
    }
    else {
      if (uVar4 != DAT_0801e218 - 0xaa) goto LAB_0801e4ce;
      pbVar5 = (byte *)(DAT_0801e3c8 * uVar6 + DAT_0801e3c4 + DAT_0801e3c8 + -0x19);
      bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 3;
      bVar2 = 0xf7;
    }
  }
  else if (uVar4 == DAT_0801e1a8) {
    pbVar5 = (byte *)(DAT_0801e2f0 * uVar6 + DAT_0801e2ec + DAT_0801e2f0 + -0x1d);
    bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 6;
    bVar2 = 0xbf;
  }
  else if ((int)DAT_0801e1a8 < (int)uVar4) {
    if (uVar4 == DAT_0801e1d4) {
      pbVar5 = (byte *)(DAT_0801e334 * uVar6 + DAT_0801e330 + DAT_0801e338);
      bVar3 = (byte)DAT_0801e1a0[2] & 1;
      bVar2 = 0xfe;
    }
    else {
      if ((int)uVar4 <= (int)DAT_0801e1d4) {
        if (uVar4 == DAT_0801e1d4 - 0x44) {
          *(ushort *)(uVar6 * DAT_0801e30c + DAT_0801e308 + DAT_0801e310) = DAT_0801e1a0[2];
        }
        goto LAB_0801e4ce;
      }
      if (uVar4 == DAT_0801e1ec) {
        pbVar5 = (byte *)(DAT_0801e35c * uVar6 + DAT_0801e358 + DAT_0801e35c + -0x1a);
        bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 1;
        bVar2 = 0xfd;
      }
      else {
        if (uVar4 != DAT_0801e1ec + 0x1d) goto LAB_0801e4ce;
        pbVar5 = (byte *)(DAT_0801e380 * uVar6 + DAT_0801e37c + DAT_0801e380 + -0x1a);
        bVar3 = ((byte)DAT_0801e1a0[2] & 7) << 2;
        bVar2 = 0xe3;
      }
    }
  }
  else if (uVar4 == DAT_0801e1a8 - 0xcc) {
    pbVar5 = (byte *)(DAT_0801e2a8 * uVar6 + DAT_0801e2a4 + DAT_0801e2a8 + -0x1d);
    bVar3 = ((byte)DAT_0801e1a0[2] & 7) << 2;
    bVar2 = 0xe3;
  }
  else if ((int)(DAT_0801e1a8 - 0xcc) < (int)uVar4) {
    if (uVar4 != DAT_0801e1b8) goto LAB_0801e4ce;
    pbVar5 = (byte *)(SUB_0801e2cc * uVar6 + DAT_0801e2c8 + SUB_0801e2cc + -0x1d);
    bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 5;
    bVar2 = 0xdf;
  }
  else {
    if (uVar4 != DAT_0801e1a8 - 0x17d) goto LAB_0801e4ce;
    pbVar5 = (byte *)(DAT_0801e280 * uVar6 + DAT_0801e27c + DAT_0801e284);
    bVar3 = ((byte)DAT_0801e1a0[2] & 1) << 1;
    bVar2 = 0xfd;
  }
  *pbVar5 = bVar2 & *pbVar5 | bVar3;
LAB_0801e4ce:
  *(byte *)(puVar1 + 0x488) = (byte)puVar1[0x488] & 0xdf;
  return in_lr;
}


// ===== 0806E634 FUN_0806e634

undefined8 FUN_0806e634(uint param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  uint uVar4;
  undefined4 in_lr;
  
  uVar4 = *(ushort *)
           ((param_1 & 0x7f) * 0x50 + ((int)(param_1 & 0x80) >> 7) * DAT_0806e6c8 + DAT_0806e6c4 +
           0x24) & 0x7fff;
  uVar3 = *(uint *)(uVar4 * 4 + DAT_0806e6cc);
  if ((((((uVar3 & 0x1f00000) >> 0x14 < 0x15) && (uVar3 = (uVar3 & 0xc0000) >> 0x12, uVar3 != 3)) &&
       (uVar3 != 2)) && ((iVar1 = FUN_080dcdc0(uVar4), 2 < iVar1 || (iVar1 < 1)))) &&
     (uVar3 = (uint)*(ushort *)(uVar4 * 2 + DAT_0806e6d0), uVar3 != DAT_0806e6d4)) {
    if ((int)DAT_0806e6d4 < (int)uVar3) {
      if (uVar3 != DAT_0806e74c) {
        if ((int)DAT_0806e74c < (int)uVar3) {
          if (uVar3 != DAT_0806e774) {
            if ((int)DAT_0806e774 < (int)uVar3) {
              if (uVar3 != DAT_0806e78c) {
                uVar4 = DAT_0806e79c;
                if ((int)uVar3 <= (int)DAT_0806e78c) {
                  uVar4 = DAT_0806e78c - 0x2f;
                }
                goto joined_r0x0806e794;
              }
            }
            else if (uVar3 != DAT_0806e774 - 0xf0) {
              uVar4 = DAT_0806e774 - 0x20;
              goto joined_r0x0806e794;
            }
          }
        }
        else if (uVar3 != DAT_0806e74c - 0xbd) {
          if ((int)uVar3 <= (int)(DAT_0806e74c - 0xbd)) {
            if ((int)uVar3 <= (int)(DAT_0806e74c - 0xbf)) {
              iVar1 = DAT_0806e74c - 0xc3;
              goto LAB_0806e744;
            }
            goto LAB_0806e7a0;
          }
          if (uVar3 != DAT_0806e75c) {
            uVar4 = DAT_0806e75c + 0x74;
            goto joined_r0x0806e794;
          }
        }
      }
    }
    else if (uVar3 != DAT_0806e6d8) {
      if ((int)DAT_0806e6d8 < (int)uVar3) {
        if (DAT_0806e708 < (int)uVar3) {
          if (uVar3 != DAT_0806e720) {
            if (((int)DAT_0806e720 <= (int)uVar3) && ((int)uVar3 <= DAT_0806e724)) {
              iVar1 = DAT_0806e724 + -2;
LAB_0806e744:
              if (iVar1 <= (int)uVar3) goto FUN_0806e796;
            }
LAB_0806e7a0:
            uVar2 = 1;
            goto LAB_0806e7a2;
          }
        }
        else if ((int)uVar3 < DAT_0806e708 + -4) {
          uVar4 = DAT_0806e708 - 0x19;
          goto joined_r0x0806e794;
        }
      }
      else if (uVar3 != DAT_0806e6dc) {
        if ((int)DAT_0806e6dc < (int)uVar3) {
          if (uVar3 != DAT_0806e6f4) {
            uVar4 = DAT_0806e6f4 + 0xfe;
            goto joined_r0x0806e794;
          }
        }
        else {
          uVar4 = DAT_0806e6e4;
          if (uVar3 != DAT_0806e6e0) {
joined_r0x0806e794:
            if (uVar3 != uVar4) goto LAB_0806e7a0;
          }
        }
      }
    }
  }
FUN_0806e796:
  uVar2 = 0;
LAB_0806e7a2:
  return CONCAT44(in_lr,uVar2);
}


// ===== 0806E7A8 FUN_0806e7a8

undefined8 FUN_0806e7a8(undefined4 param_1,uint param_2)

{
  byte bVar1;
  short sVar2;
  int iVar3;
  undefined4 uVar4;
  uint uVar5;
  uint uVar6;
  undefined4 in_lr;
  
  uVar6 = *(ushort *)
           ((param_2 & 0x7f) * 0x50 + DAT_0806e848 * ((int)(param_2 & 0x80) >> 7) + SUB_0806e844 +
           0x24) & 0x7fff;
  uVar5 = *(uint *)(uVar6 * 4 + DAT_0806e84c);
  if (((((uVar5 & 0x1f00000) >> 0x14 < 0x15) && (uVar5 = (uVar5 & 0xc0000) >> 0x12, uVar5 != 3)) &&
      (uVar5 != 2)) && ((iVar3 = FUN_080dcdc0(uVar6), 2 < iVar3 || (iVar3 < 1)))) {
    uVar5 = (uint)*(ushort *)(uVar6 * 2 + DAT_0806e850);
    if (DAT_0806e854 < (int)uVar5) {
      if (uVar5 != DAT_0806e8f4) {
        if ((int)DAT_0806e8f4 < (int)uVar5) {
          if (uVar5 != DAT_0806e930) {
            if ((int)DAT_0806e930 < (int)uVar5) {
              if (uVar5 != DAT_0806e950) {
                uVar6 = DAT_0806e95c;
                if ((int)uVar5 <= (int)DAT_0806e950) {
                  uVar6 = DAT_0806e950 - 0x2f;
                }
                goto joined_r0x0806e958;
              }
            }
            else if (uVar5 != DAT_0806e930 - 0x49) {
              uVar6 = DAT_0806e938;
              if ((int)uVar5 <= (int)(DAT_0806e930 - 0x49)) {
                uVar6 = DAT_0806e930 - 0xeb;
              }
              goto joined_r0x0806e958;
            }
          }
        }
        else if (uVar5 != DAT_0806e8f4 - 0xf9) {
          if ((int)(DAT_0806e8f4 - 0xf9) < (int)uVar5) {
            if (uVar5 != DAT_0806e908) {
              uVar6 = DAT_0806e910;
              if ((int)uVar5 <= (int)DAT_0806e908) {
                uVar6 = DAT_0806e908 - 0x74;
              }
              goto joined_r0x0806e958;
            }
          }
          else if ((uVar5 != DAT_0806e8f4 - 0x148) &&
                  ((((int)uVar5 < (int)(DAT_0806e8f4 - 0x148) ||
                    ((int)(DAT_0806e8f4 - 0xfb) < (int)uVar5)) ||
                   ((int)uVar5 < (int)(DAT_0806e8f4 - 0xff))))) {
LAB_0806e98c:
            bVar1 = *(byte *)((param_2 & 0x7f) * 0x50 + DAT_0806e9d0 * ((int)(param_2 & 0x80) >> 7)
                              + DAT_0806e9cc + 0x31) & 0xf;
            if (bVar1 < 5) {
              iVar3 = count_empty_field_slots(param_1);
              if (0 < iVar3) goto LAB_0806e9de;
            }
            else if (bVar1 < 7) {
              iVar3 = FUN_08010fa4(param_1,0xff,1,0xff);
              if (0 < iVar3) {
LAB_0806e9fe:
                sVar2 = FUN_0806df2c(param_1);
                if (sVar2 != 0) {
                  uVar4 = 5;
                  goto LAB_0806ea14;
                }
                goto LAB_0806ea0a;
              }
            }
            else {
              iVar3 = FUN_08010fa4(param_1,0xff,1,0xff);
              if (1 < iVar3) goto LAB_0806e9fe;
            }
          }
        }
      }
    }
    else if (((int)uVar5 < DAT_0806e854 + -2) && (uVar5 != DAT_0806e858)) {
      if ((int)DAT_0806e858 < (int)uVar5) {
        if (DAT_0806e89c < (int)uVar5) {
          if (uVar5 != DAT_0806e8b4) {
            uVar6 = DAT_0806e8bc;
            if ((int)DAT_0806e8b4 < (int)uVar5) goto joined_r0x0806e958;
            if (uVar5 != DAT_0806e8b4 - 0x21) goto LAB_0806e98c;
            iVar3 = count_empty_field_slots(param_1);
            if (iVar3 < 1) goto FUN_0806ea12;
            iVar3 = FUN_08010bec(param_1);
            if (0 < iVar3) goto LAB_0806ea0a;
LAB_0806e9de:
            sVar2 = FUN_0806df2c(param_1);
            if (sVar2 != 0) {
              uVar4 = 3;
              goto LAB_0806ea14;
            }
            goto LAB_0806ea0a;
          }
        }
        else if ((int)uVar5 < DAT_0806e89c + -4) {
          uVar6 = DAT_0806e89c - 0x19;
          goto joined_r0x0806e958;
        }
      }
      else {
        if (uVar5 == DAT_0806e85c) {
          sVar2 = FUN_0806dfe8(param_1);
          if (sVar2 == 0) goto FUN_0806ea12;
          FUN_0806df2c(param_1);
LAB_0806ea0a:
          uVar4 = 1;
          goto LAB_0806ea14;
        }
        if ((int)DAT_0806e85c < (int)uVar5) {
          if (uVar5 != DAT_0806e878) {
            uVar6 = DAT_0806e884;
            if ((int)uVar5 <= (int)DAT_0806e878) {
              uVar6 = DAT_0806e87c;
            }
            goto joined_r0x0806e958;
          }
        }
        else {
          uVar6 = DAT_0806e864;
          if (uVar5 != DAT_0806e860) {
joined_r0x0806e958:
            if (uVar5 != uVar6) goto LAB_0806e98c;
          }
        }
      }
    }
  }
FUN_0806ea12:
  uVar4 = 0;
LAB_0806ea14:
  return CONCAT44(in_lr,uVar4);
}


// ===== 08074B2C FUN_08074b2c

undefined8 FUN_08074b2c(byte *param_1,int param_2,uint param_3,uint param_4)

{
  byte bVar1;
  byte bVar2;
  byte *pbVar3;
  uint uVar4;
  int iVar5;
  undefined4 in_lr;
  
  iVar5 = 0;
  pbVar3 = param_1;
  if (0 < param_2) {
    do {
      if (*pbVar3 == param_3) goto LAB_08074c14;
      iVar5 = iVar5 + 1;
      pbVar3 = pbVar3 + 2;
    } while (iVar5 < param_2);
  }
  if (param_4 == 1) {
    bVar1 = *(byte *)((param_3 & 0x7f) * 0x50 + DAT_08074b90 * ((int)(param_3 & 0x80) >> 7) +
                      DAT_08074b8c + 0x31);
    bVar2 = bVar1 & 0xf;
    if (((bVar1 & 0xf) == 0) || ((4 < bVar2 && (param_4 = 2, 6 < bVar2)))) {
      param_4 = 3;
    }
  }
  else if (param_4 == 8) {
    uVar4 = (uint)*(ushort *)
                   ((*(ushort *)
                      ((param_3 & 0x7f) * 0x50 + DAT_08074be8 * ((int)(param_3 & 0x80) >> 7) +
                       DAT_08074be4 + 0x24) & 0x7fff) * 2 + DAT_08074be0);
    if (SUB_08074bec < (int)uVar4) {
      if ((uVar4 != DAT_08074c1c) && (uVar4 != DAT_08074c1c + 0x19)) goto LAB_08074c02;
    }
    else if ((((int)uVar4 < SUB_08074bec + -4) && (uVar4 != DAT_08074bf0)) &&
            ((((int)uVar4 < (int)DAT_08074bf0 || ((int)(DAT_08074bf0 + 0x21) < (int)uVar4)) ||
             ((int)uVar4 < (int)(DAT_08074bf0 + 0x1d))))) goto LAB_08074c02;
    param_4 = 7;
  }
LAB_08074c02:
  *(ushort *)(param_1 + param_2 * 2) = (ushort)param_3 & 0xff | (ushort)((param_4 & 0xff) << 8);
  param_2 = param_2 + 1;
LAB_08074c14:
  return CONCAT44(in_lr,param_2);
}


// ===== 08019884 FUN_08019884

/* WARNING: Removing unreachable block (ram,0x08019b54) */

undefined4 FUN_08019884(uint param_1)

{
  uint uVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined4 in_lr;
  
  cleanup_card_actions();
  iVar5 = 0;
  iVar3 = DAT_08019908;
  iVar4 = DAT_08019904;
  if ((*(byte *)((param_1 & 0x7f) * 0x50 + DAT_08019908 * ((int)(param_1 & 0x80) >> 7) +
                 DAT_08019904 + 0x3e) & 0xf) != 0) {
    do {
      uVar1 = (*(ushort *)
                (iVar5 * 2 + (param_1 & 0x7f) * 0x50 + iVar3 * ((int)(param_1 & 0x80) >> 7) +
                iVar4 + 0x40) >> 8 & 0xf) - 1;
      if (uVar1 < 8) {
                    /* WARNING: Could not recover jumptable at 0x08019900. Too many branches */
                    /* WARNING: Treating indirect jump as call */
        uVar2 = (**(code **)(uVar1 * 4 + DAT_0801990c))();
        return uVar2;
      }
      iVar5 = iVar5 + 1;
      iVar3 = DAT_08019bd8;
      iVar4 = DAT_08019bd4;
    } while (iVar5 < (int)(*(byte *)((param_1 & 0x7f) * 0x50 +
                                     DAT_08019bd8 * ((int)(param_1 & 0x80) >> 7) + DAT_08019bd4 +
                                    0x3e) & 0xf));
  }
  process_card_actions();
  return in_lr;
}


// ===== 0802F73C FUN_0802f73c

undefined4 FUN_0802f73c(uint param_1,short param_2,int param_3)

{
  ushort uVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  ushort *puVar9;
  int iVar10;
  undefined4 in_lr;
  
  iVar10 = DAT_0802f7a0;
  iVar4 = (param_1 & 0x7f) * 0x50 + DAT_0802f7a4 * ((int)(param_1 & 0x80) >> 7);
  iVar7 = iVar4 + DAT_0802f7a0;
  uVar5 = (uint)*(ushort *)((*(ushort *)(iVar7 + 0x24) & 0x7fff) * 2 + DAT_0802f79c);
  if (uVar5 != DAT_0802f7a8) {
    if ((int)uVar5 <= (int)DAT_0802f7a8) {
      if (uVar5 == DAT_0802f7ac) {
        uVar5 = (uint)*(byte *)(iVar7 + 0x3c);
        if (uVar5 == 0xff) {
          return in_lr;
        }
        uVar2 = *(uint *)((uVar5 & 0x7f) * 0x50 + DAT_0802f874 * ((int)(uVar5 & 0x80) >> 7) +
                          DAT_0802f7a0 + 0x30);
        if (((uVar2 & 0xfffff) >> 0xc & 0x7f) != 0) {
          return in_lr;
        }
        uVar6 = (*(uint *)(iVar7 + 0x30) & 0xfffff) >> 0x13;
        if (param_2 != 0) {
          uVar6 = 1 - uVar6;
        }
        if (uVar6 == (uVar2 & 0xfffff) >> 0x13) {
          return in_lr;
        }
        puVar9 = (ushort *)(uVar6 * 2 + param_3);
        iVar10 = FUN_08011074(uVar6,*puVar9);
        if (iVar10 != -1) {
          uVar1 = FUN_0801a8a4(uVar5,*puVar9);
          *puVar9 = uVar1 | *puVar9;
          return in_lr;
        }
        uVar3 = send_card_to_graveyard
                          (uVar5,((*(uint *)(iVar7 + 0x30) & 0xfffff) >> 0x13) << 0xf | 0x41,
                           param_1 & 0xffff);
        return uVar3;
      }
      if (uVar5 != DAT_0802f7b0) {
        return in_lr;
      }
      iVar8 = 0;
      if ((*(byte *)(iVar7 + 0x3e) & 0xf) == 0) {
        return in_lr;
      }
      do {
        uVar1 = *(ushort *)(iVar4 + iVar10 + 0x40);
        if (uVar1 >> 8 == 3) {
          uVar3 = 0x23;
          if (((*(uint *)(iVar7 + 0x30) & 0xfffff) >> 0xc & 0x80) != 0) {
            uVar3 = DAT_0802f8e8;
          }
          drawing_FUN_08022034(uVar3,uVar1 & 0xff,param_2 == 0);
        }
        iVar4 = iVar4 + 2;
        iVar8 = iVar8 + 1;
      } while (iVar8 < (int)(*(byte *)(iVar7 + 0x3e) & 0xf));
      return in_lr;
    }
    if (uVar5 != DAT_0802f7cc) {
      if ((int)DAT_0802f7cc < (int)uVar5) {
        if (uVar5 != DAT_0802f7dc) {
          return in_lr;
        }
        uVar5 = *(uint *)(iVar7 + 0x30) & 0xfffff;
        if ((uVar5 >> 0xc & 0x7f) != 0) {
          return in_lr;
        }
        if (param_2 == 0) {
          return in_lr;
        }
        uVar3 = send_card_to_graveyard(param_1,(uVar5 >> 0x13) << 0xf | 0x41,param_1 & 0xffff);
        return uVar3;
      }
      if (uVar5 != DAT_0802f7cc - 0xf9) {
        return in_lr;
      }
    }
  }
  iVar10 = DAT_0802f7a0 + (param_1 & 0x7f) * 0x50 + DAT_0802f950 * ((int)(param_1 & 0x80) >> 7);
  uVar5 = *(uint *)(iVar10 + 0x30) & 0xfffff;
  if (((uVar5 >> 0xc & 0x7f) == 0) && (param_2 != 0)) {
    uVar5 = uVar5 >> 0x13;
    puVar9 = (ushort *)(uVar5 * 2 + param_3);
    uVar2 = FUN_080110dc(uVar5,*puVar9);
    if (uVar2 == 0xffffffff) {
      uVar3 = send_card_to_graveyard(param_1,uVar5 << 0xf | 0x41,param_1 & 0xffff);
      return uVar3;
    }
    FUN_080188ac(param_1,uVar5 << 0xf | (uVar2 & 0x3f) << 4 | 0x1400 |
                         ((*(byte *)(iVar10 + 0x33) & 0x1f) >> 4) << 3);
    *puVar9 = (ushort)(1 << (uVar2 + 5 & 0xff)) | *puVar9;
  }
  return in_lr;
}


// ===== 08072598 FUN_08072598

undefined4 FUN_08072598(int param_1)

{
  undefined2 uVar1;
  undefined1 *puVar2;
  undefined1 *puVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  undefined4 in_lr;
  
  if (5 < *(int *)(param_1 + 0x10)) {
    uVar1 = get_ordinal_id(DAT_080726ac);
    FUN_0800f9dc(1,uVar1);
  }
  if (7 < *(int *)(param_1 + 0x10)) {
    uVar1 = get_ordinal_id(DAT_080726ac);
    FUN_0800f9dc(1,uVar1);
  }
  if (3 < *(int *)(param_1 + 0x14)) {
    uVar1 = get_ordinal_id(DAT_080726b0);
    FUN_0800f9dc(1,uVar1);
  }
  if (5 < *(int *)(param_1 + 0x14)) {
    uVar1 = get_ordinal_id(DAT_080726b0);
    FUN_0800f9dc(1,uVar1);
  }
  if (7 < *(int *)(param_1 + 0x14)) {
    uVar1 = get_ordinal_id(DAT_080726b4);
    FUN_0800f9dc(1,uVar1);
  }
  if (5 < *(int *)(param_1 + 4)) {
    uVar1 = get_ordinal_id(DAT_080726b8);
    FUN_0800f9dc(1,uVar1);
    uVar1 = get_ordinal_id(DAT_080726bc);
    FUN_0800f9dc(1,uVar1);
    uVar1 = get_ordinal_id(0x1200);
    FUN_0800f9dc(1,uVar1);
    uVar1 = get_ordinal_id(DAT_080726c0);
    FUN_0800f9dc(1,uVar1);
  }
  iVar5 = 0;
  iVar6 = 0;
  iVar4 = DAT_080726c4;
  if ((*(byte *)(DAT_080726c4 + DAT_080726c8) & 0x7f) != 0) {
    do {
      puVar3 = (undefined1 *)
               (uint)*(ushort *)((*(ushort *)(iVar4 + DAT_080726d4) & 0x7fff) * 2 + DAT_080726d0);
      if (puVar3 == DAT_080726cc) {
LAB_0807271e:
        iVar6 = iVar6 + 1;
      }
      else {
        if ((int)puVar3 <= (int)DAT_080726cc) {
          if (puVar3 != &DAT_00001400) {
            if (&DAT_00001400 < puVar3) {
              if (puVar3 != DAT_080726f0) {
                puVar2 = DAT_080726f0 + 0x62;
                goto LAB_080726e8;
              }
            }
            else {
              puVar2 = DAT_080726dc;
              if (puVar3 != DAT_080726d8) {
LAB_080726e8:
                if (puVar3 != puVar2) goto LAB_08072720;
              }
            }
          }
          goto LAB_0807271e;
        }
        if (DAT_08072710 < (int)puVar3) {
          if (puVar3 == DAT_08072860) goto LAB_0807271e;
        }
        else if ((DAT_08072710 + -2 <= (int)puVar3) ||
                (((int)puVar3 <= DAT_08072714 && (DAT_08072714 + -3 <= (int)puVar3))))
        goto LAB_0807271e;
      }
LAB_08072720:
      iVar5 = iVar5 + 1;
      iVar4 = iVar4 + 0x50;
    } while (iVar5 < (int)(*(byte *)(DAT_080726c4 + DAT_080726c8) & 0x7f));
  }
  if (0 < iVar6) {
    if (iVar6 < 4) goto LAB_08072748;
    iVar6 = 3;
    do {
      uVar1 = get_ordinal_id(DAT_08072864);
      FUN_0800f9dc(1,uVar1);
      iVar6 = iVar6 + -1;
LAB_08072748:
    } while (iVar6 != 0);
  }
  uVar1 = get_ordinal_id(DAT_08072868);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_0807286c);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072870);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072874);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072878);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_0807287c);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072880);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072884);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072888);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_0807288c);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072890);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072894);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_08072898);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_0807289c);
  FUN_0800f9dc(1,uVar1);
  uVar1 = get_ordinal_id(DAT_080728a0);
  FUN_0800f9dc(1,uVar1);
  return in_lr;
}



// ===== 0801F980 FUN_0801f980

undefined8 FUN_0801f980(uint param_1,uint param_2)

{
  ushort uVar1;
  short sVar2;
  int iVar3;
  ushort *puVar4;
  undefined4 uVar5;
  int iVar6;
  int iVar7;
  uint uVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  undefined4 in_lr;
  undefined8 uVar12;
  
  uVar8 = *(ushort *)
           ((param_2 & 0x7f) * 0x50 + DAT_0801f9e8 * ((int)(param_2 & 0x80) >> 7) + DAT_0801f9e4 +
           0x24) & 0x7fff;
  iVar10 = 1 - param_1;
  iVar3 = FUN_08010bec(iVar10);
  if (iVar3 == 0) {
    if ((*(ushort *)(uVar8 * 2 + DAT_0801f9ec) != DAT_0801f9f0) &&
       (iVar3 = FUN_0801231c(param_2,DAT_0801f9f4,1,0x10), iVar3 == 0)) goto LAB_0801fb5c;
LAB_0801fc3e:
    uVar5 = 0;
  }
  else {
    uVar8 = (uint)*(ushort *)(uVar8 * 2 + DAT_0801fa2c);
    if ((int)uVar8 <= DAT_0801fa30) {
      if (((int)uVar8 < DAT_0801fa30 + -1) && (uVar8 != DAT_0801fa34)) {
        if ((int)DAT_0801fa34 < (int)uVar8) {
          if (uVar8 != DAT_0801fa50) {
            if ((int)DAT_0801fa50 < (int)uVar8) {
              if (uVar8 == DAT_0801fa64) {
                uVar12 = FUN_0800e158(param_2,0xe);
                return uVar12;
              }
              if (uVar8 == DAT_0801fa64 + 0xf6) {
                sVar2 = FUN_0801f770(iVar10);
                goto LAB_0801faea;
              }
            }
            else if (uVar8 == DAT_0801fa50 - 0x93) goto LAB_0801fb5c;
            goto LAB_0801faf0;
          }
        }
        else if (uVar8 != DAT_0801fa34 - 0x23) {
          if ((int)(DAT_0801fa34 - 0x23) <= (int)uVar8) {
            iVar3 = DAT_0801fa34 - 0x18;
            goto LAB_0801fa7e;
          }
          goto LAB_0801faf0;
        }
      }
      goto LAB_0801fb5c;
    }
    if (uVar8 == DAT_0801fa8c) {
      sVar2 = FUN_0801f7f4(iVar10);
LAB_0801faea:
      if (sVar2 == 0) {
LAB_0801faf0:
        iVar3 = FUN_080dcdc0(*(ushort *)
                              ((param_2 & 0x7f) * 0x50 + DAT_0801fb28 * ((int)(param_2 & 0x80) >> 7)
                               + DAT_0801fb24 + 0x24) & 0x7fff);
        if ((iVar3 < 1) ||
           (((2 < iVar3 &&
             ((iVar3 != 3 ||
              (iVar3 = show_confirmation_prompt
                                 (DAT_0801fb60,0xff,1 << (param_1 & 0xff) & 0xffff,0x20,0xe,1),
              iVar3 == 0)))) || (sVar2 = FUN_0801100c(1 - param_1), sVar2 != 0)))) {
          iVar7 = (param_2 & 0x7f) * 0x50;
          iVar6 = (int)(param_2 & 0x80) >> 7;
          iVar9 = 0;
          iVar3 = iVar7;
          iVar10 = DAT_0801fbbc;
          iVar11 = DAT_0801fbb8;
          if ((*(byte *)(iVar7 + DAT_0801fbbc * iVar6 + DAT_0801fbb8 + 0x3e) & 0xf) != 0) {
            do {
              puVar4 = (ushort *)(iVar3 + iVar6 * DAT_0801fbbc + DAT_0801fbb8 + 0x40);
              uVar8 = (uint)(byte)*puVar4;
              uVar1 = *puVar4 >> 8;
              if (uVar1 == 1) {
                if (*(ushort *)
                     ((*(ushort *)
                        ((uVar8 & 0x7f) * 0x50 + iVar10 * ((int)(uVar8 & 0x80) >> 7) + iVar11 + 0x24
                        ) & 0x7fff) * 2 + DAT_0801fbc0) == DAT_0801fbf0) goto LAB_0801fb5c;
              }
              else if ((uVar1 == 4) &&
                      (*(ushort *)
                        ((*(ushort *)
                           ((uVar8 & 0x7f) * 0x50 + ((int)(uVar8 & 0x80) >> 7) * DAT_0801fbbc +
                            DAT_0801fc50 + 0x24) & 0x7fff) * 2 + DAT_0801fbc0) == DAT_0801fc54))
              goto LAB_0801fb5c;
              iVar9 = iVar9 + 1;
              iVar3 = iVar3 + 2;
              iVar10 = DAT_0801fc58;
              iVar11 = DAT_0801fc50;
            } while (iVar9 < (int)(*(byte *)(DAT_0801fc58 * iVar6 + iVar7 + DAT_0801fc50 + 0x3e) &
                                  0xf));
          }
          goto LAB_0801fc3e;
        }
      }
    }
    else {
      if ((int)DAT_0801fa8c < (int)uVar8) {
        if (uVar8 != DAT_0801faa4) {
          if ((int)DAT_0801faa4 < (int)uVar8) {
            if (uVar8 == SUB_0801fab8) goto LAB_0801fb5c;
            if (uVar8 == SUB_0801fab8 + 0x40) {
              sVar2 = FUN_0801f928(param_1);
              goto LAB_0801faea;
            }
          }
          else if (uVar8 == DAT_0801faa4 - 4) {
            sVar2 = FUN_0801f884(iVar10);
            goto LAB_0801faea;
          }
          goto LAB_0801faf0;
        }
        sVar2 = FUN_0801f900();
        goto LAB_0801faea;
      }
      if (uVar8 != DAT_0801fa8c - 0xbc) {
        if ((int)(DAT_0801fa8c - 0xbc) <= (int)uVar8) {
          iVar3 = DAT_0801fa8c - 0x22;
LAB_0801fa7e:
          if (((int)uVar8 <= iVar3) && (iVar3 + -1 <= (int)uVar8)) goto LAB_0801fb5c;
        }
        goto LAB_0801faf0;
      }
    }
LAB_0801fb5c:
    uVar5 = 1;
  }
  return CONCAT44(in_lr,uVar5);
}


// ===== 0801401E FUN_0801401e

void FUN_0801401e(void)

{
  byte bVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  uint uVar7;
  uint uVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  ushort *unaff_r7;
  byte *pbVar12;
  uint in_stack_0000002c;
  uint in_stack_00000030;
  int in_stack_00000034;
  uint in_stack_00000038;
  
  iVar3 = DAT_080148e0;
  if (((in_stack_0000002c & 0x7f) - 100 & 0xff) < 0x1b) {
    FUN_080152b0();
    return;
  }
  uVar7 = (uint)*(ushort *)((uint)*unaff_r7 * 2 + DAT_08014090);
  if (uVar7 == DAT_08014094) {
LAB_080145f4:
    if ((in_stack_00000030 & 1) == 0) {
      FUN_080152b0();
      return;
    }
    iVar3 = 0;
    do {
      uVar7 = DAT_0801467c;
      iVar6 = DAT_08014674;
      iVar11 = DAT_08014670;
      iVar10 = 0;
      iVar9 = iVar3 + 1;
      if ((*(uint *)(DAT_08014670 * iVar3 + DAT_08014674 + 0x1c) & 0xfffff) >> 0xd != 0) {
        iVar4 = DAT_08014678 + DAT_08014674;
        iVar5 = DAT_08014670 * iVar3 + DAT_08014674;
        do {
          uVar8 = (uint)*(byte *)(iVar10 + iVar3 * iVar11 + iVar4);
          uVar8 = (uint)*(ushort *)
                         ((*(ushort *)
                            ((uVar8 & 0x7f) * 0x50 +
                             -((int)((uVar8 & 0x80) << 0x18) >> 0x1f) * iVar11 + iVar6 + 0x24) &
                          0x7fff) * 2 + DAT_08014680);
          if (uVar8 == uVar7) {
LAB_0801468e:
            *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + 300;
          }
          else {
            uVar2 = DAT_080146b0;
            if ((int)uVar8 <= (int)uVar7) {
              uVar2 = DAT_08014684;
            }
            if (uVar8 == uVar2) goto LAB_0801468e;
          }
          iVar10 = iVar10 + 1;
        } while (iVar10 < (int)((*(uint *)(iVar5 + 0x1c) & 0xfffff) >> 0xd));
      }
      iVar3 = iVar9;
      if (1 < iVar9) {
        FUN_080152b0();
        return;
      }
    } while( true );
  }
  if ((int)DAT_08014094 < (int)uVar7) {
    uVar8 = DAT_080141d0;
    if (uVar7 == DAT_080141d0) {
      uVar8 = FUN_08014e94();
    }
    if ((int)uVar8 < (int)uVar7) {
      uVar8 = DAT_08014270;
      if (uVar7 == DAT_08014270) {
        uVar8 = FUN_080150bc();
      }
      if ((int)uVar8 < (int)uVar7) {
        uVar8 = DAT_080142b8;
        if (uVar7 == DAT_080142b8) {
          uVar8 = FUN_08015182();
        }
        if ((int)uVar8 < (int)uVar7) {
          uVar8 = DAT_080142d4;
          if (uVar7 == DAT_080142d4) {
            uVar8 = FUN_080151c4();
          }
          if (uVar7 == uVar8 + 0x34) {
            FUN_08015200();
          }
          FUN_080152b0();
          return;
        }
        uVar8 = uVar8 - 0x44;
        if (uVar7 == uVar8) {
          uVar8 = FUN_08015078();
        }
        if (uVar7 == uVar8 + 0x15) {
          FUN_08015140();
        }
        FUN_080152b0();
        return;
      }
      uVar8 = uVar8 - 0xa7;
      if (uVar7 == uVar8) {
        uVar8 = FUN_08015018();
      }
      if ((int)uVar8 < (int)uVar7) {
        uVar8 = DAT_0801428c;
        if (uVar7 == DAT_0801428c) {
          uVar8 = FUN_0801503c();
        }
        if (uVar7 == uVar8 + 0x35) {
          FUN_08015078();
        }
        FUN_080152b0();
        return;
      }
      uVar8 = uVar8 - 10;
      if (uVar7 == uVar8) {
        uVar8 = FUN_08014f18();
      }
      if (uVar7 == uVar8 + 8) {
        FUN_08014fb8();
      }
      FUN_080152b0();
      return;
    }
    uVar8 = DAT_080141d4;
    if (uVar7 == DAT_080141d4) {
      uVar8 = FUN_08014d2c();
    }
    if ((int)uVar8 < (int)uVar7) {
      uVar8 = DAT_0801421c;
      if (uVar7 == DAT_0801421c) {
        uVar8 = FUN_08014dc2();
      }
      if ((int)uVar8 < (int)uVar7) {
        uVar8 = DAT_08014238;
        if (uVar7 == DAT_08014238) {
          uVar8 = FUN_08014dfc();
        }
        if (uVar7 == uVar8 + 0x40) {
          FUN_08014e6c();
        }
        FUN_080152b0();
        return;
      }
      uVar8 = uVar8 - 0xe6;
      if (uVar7 == uVar8) {
        uVar8 = FUN_08014d64();
      }
      if (uVar7 == uVar8 + 0xc) {
        FUN_08014da4();
      }
      FUN_080152b0();
      return;
    }
    if (uVar7 == uVar8 - 0x1b) {
LAB_080146e6:
      iVar3 = DAT_080147e0;
      if ((in_stack_00000030 & 1) != 0) {
        iVar11 = 0;
        do {
          iVar6 = DAT_080147e8;
          iVar10 = 0;
          iVar9 = iVar11 + 1;
          if ((*(uint *)(iVar11 * iVar3 + DAT_080147e4 + 0x1c) & 0xfffff) >> 0xd != 0) {
            pbVar12 = (byte *)(DAT_080147e0 * iVar11 + DAT_080147e4 + DAT_080147ec);
            iVar4 = iVar3;
            do {
              bVar1 = *pbVar12;
              if ((bVar1 != 0xff) &&
                 ((*(uint *)((*(ushort *)
                               ((bVar1 & 0x7f) * 0x50 + iVar4 * (uint)(bVar1 >> 7) + DAT_080147e4 +
                               0x24) & 0x7fff) * 4 + iVar6) & 0x1f00000) == 0x100000)) {
                *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + 500;
              }
              pbVar12 = pbVar12 + 1;
              iVar10 = iVar10 + 1;
              iVar4 = DAT_080147e0;
            } while (iVar10 < (int)((*(uint *)(DAT_080147e0 * iVar11 + DAT_080147e4 + 0x1c) &
                                    0xfffff) >> 0xd));
          }
          pbVar12 = (byte *)(iVar11 * 0xb + DAT_080147e4 + DAT_080147f0);
          iVar11 = 4;
          do {
            bVar1 = *pbVar12;
            if (((bVar1 != 0xff) &&
                (iVar6 = (bVar1 & 0x7f) * 0x50 + (uint)(bVar1 >> 7) * iVar3 + DAT_080147e4,
                (*(byte *)(iVar6 + 0x30) & 0x1f) == 1)) &&
               ((int)((uint)*(byte *)(iVar6 + 0x33) * 0x8000000) < 0)) {
              *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + 500;
            }
            pbVar12 = pbVar12 + 1;
            iVar11 = iVar11 + -1;
          } while (-1 < iVar11);
          iVar11 = iVar9;
        } while (iVar9 < 2);
        FUN_080152b0();
        return;
      }
      FUN_080152b0();
      return;
    }
    if ((int)(uVar8 - 0x1b) < (int)uVar7) {
      uVar8 = DAT_080141f0;
      if (uVar7 == DAT_080141f0) {
        uVar8 = FUN_08014c4c();
      }
      if (uVar7 == uVar8 + 8) {
        FUN_08014cf4();
      }
      FUN_080152b0();
      return;
    }
    uVar8 = uVar8 - 0xca;
    if (uVar7 == uVar8) {
      uVar8 = FUN_08014c10();
    }
    if (uVar7 != uVar8 + 0x30) {
      FUN_080152b0();
      return;
    }
    if ((in_stack_00000030 & 1) == 0) {
      FUN_080152b0();
      return;
    }
    iVar3 = FUN_08010cdc(in_stack_00000038,1,in_stack_0000002c);
    FUN_080152a8(iVar3,iVar3 * 0x7d);
  }
  else {
    if (uVar7 == DAT_08014098) {
      if ((in_stack_00000030 & 3) != 0) {
        FUN_08015178((uint)*(byte *)((in_stack_0000002c & 0x7f) * 0x50 +
                                     DAT_0801453c *
                                     -((int)((in_stack_0000002c & 0x80) << 0x18) >> 0x1f) +
                                     DAT_08014538 + 0x3a) * 0x7d);
        return;
      }
      FUN_080152b0();
      return;
    }
    if ((int)uVar7 <= (int)DAT_08014098) {
      uVar8 = DAT_0801409c;
      if (uVar7 == DAT_0801409c) {
        uVar8 = FUN_080149a4();
      }
      iVar6 = DAT_080143dc;
      iVar11 = DAT_080143d8;
      iVar3 = DAT_080143d4;
      if ((int)uVar8 < (int)uVar7) {
        if (uVar7 == DAT_080140dc) {
          if ((in_stack_00000030 & 1) != 0) {
            iVar3 = show_confirmation_prompt
                              (DAT_0801434c,0xff,1 << (in_stack_00000038 & 0xff) & 0xffff,1);
            FUN_0801517a(iVar3 * 500);
            return;
          }
          FUN_080152b0();
          return;
        }
        if ((int)DAT_080140dc < (int)uVar7) {
          if (uVar7 == DAT_080140f4) goto LAB_080145f4;
          if (uVar7 != DAT_080140f4 + 2) {
            FUN_080152b0();
            return;
          }
          if ((in_stack_00000030 & 1) == 0) {
            FUN_080152b0();
            return;
          }
          iVar3 = FUN_08010d64(0,10);
          *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + iVar3 * 200;
          iVar3 = FUN_08010d64(1,10);
          FUN_080152aa(iVar3,iVar3 * 200);
          goto LAB_080146e6;
        }
        if (uVar7 == DAT_080140dc - 0x3d) goto LAB_08014572;
        if (uVar7 != DAT_080140dc - 0x26) {
          FUN_080152b0();
          return;
        }
        if ((in_stack_00000030 & 3) == 0) {
          FUN_080152b0();
          return;
        }
        iVar3 = DAT_080145f0 * in_stack_00000038 + DAT_080145ec;
        *(uint *)(unaff_r7 + 2) =
             *(int *)(unaff_r7 + 2) +
             ((*(byte *)(iVar3 + 0x1c) & 0x3f) << 1 | (uint)(*(byte *)(iVar3 + 0x1b) >> 7)) * 300;
        iVar3 = ((*(byte *)(iVar3 + 0x1c) & 0x3f) << 1 | (uint)(*(byte *)(iVar3 + 0x1b) >> 7)) * 300
        ;
      }
      else {
        if (uVar7 == uVar8 - 0x6e) {
          if ((in_stack_00000030 & 1) == 0) {
            FUN_080152b0();
            return;
          }
          iVar10 = 0;
          iVar9 = DAT_080143d4 * in_stack_00000038 + DAT_080143d8;
          if ((*(uint *)(iVar9 + 0x1c) & 0xfffff) >> 0xd != 0) {
            pbVar12 = (byte *)(DAT_080143d4 * in_stack_00000038 + DAT_080143d8 + DAT_080143e0);
            do {
              if ((*(uint *)((*(ushort *)
                               ((*pbVar12 & 0x7f) * 0x50 +
                                -((int)((*pbVar12 & 0x80) << 0x18) >> 0x1f) * iVar3 + iVar11 + 0x24)
                             & 0x7fff) * 4 + iVar6) & 0x1f00000) >> 0x14 < 0x15) {
                *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + 100;
              }
              pbVar12 = pbVar12 + 1;
              iVar10 = iVar10 + 1;
            } while (iVar10 < (int)((*(uint *)(iVar9 + 0x1c) & 0xfffff) >> 0xd));
            FUN_080152b0();
            return;
          }
          FUN_080152b0();
          return;
        }
        if ((int)(uVar8 - 0x6e) < (int)uVar7) {
          if (uVar7 != DAT_080140b8) {
            if (uVar7 != DAT_080140b8 + 0x15) {
              FUN_080152b0();
              return;
            }
            if ((in_stack_00000030 & 1) == 0) {
              FUN_080152b0();
              return;
            }
            iVar3 = FUN_08010d64(0,7);
            *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + iVar3 * 100;
            iVar3 = FUN_08010d64(1,7);
            FUN_080152aa(iVar3,iVar3 * 100);
LAB_08014572:
            if ((in_stack_00000030 & 1) != 0) {
              FUN_0801517a(in_stack_00000034 * 500);
              return;
            }
            FUN_080152b0();
            return;
          }
        }
        else {
          if (uVar7 == DAT_080140a0) {
            if ((in_stack_00000030 & 1) != 0) {
              iVar3 = show_confirmation_prompt
                                (DAT_08014310,0xff,1 << (in_stack_00000038 & 0xff) & 0xffff,1);
              FUN_0801517a(iVar3 * 500);
              return;
            }
            FUN_080152b0();
            return;
          }
          if (uVar7 != DAT_080140a0 + 0xdf) {
            FUN_080152b0();
            return;
          }
          if ((in_stack_00000030 & 1) == 0) {
            FUN_080152b0();
            return;
          }
          iVar3 = FUN_08010d64(0,0xd);
          *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + iVar3 * 100;
          iVar3 = FUN_08010d64(1,0xd);
          FUN_080152aa(iVar3,iVar3 * 100);
        }
        if ((in_stack_00000030 & 3) == 0) {
          FUN_080152b0();
          return;
        }
        iVar3 = show_confirmation_prompt(DAT_0801449c,0xff,3,1);
        iVar11 = show_confirmation_prompt(DAT_080144a0,0xff,3,1);
        iVar6 = show_confirmation_prompt(DAT_080144a4,0xff,3,1);
        iVar9 = show_confirmation_prompt(DAT_080144a8,0xff,3,1);
        iVar10 = show_confirmation_prompt(DAT_080144ac,0xff,3,1);
        iVar3 = (iVar3 + iVar11 + iVar6 + iVar9 + iVar10) * 300;
        *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + iVar3;
      }
      *(int *)(unaff_r7 + 4) = *(int *)(unaff_r7 + 4) + iVar3;
      FUN_080152b0();
      return;
    }
    if (uVar7 != DAT_08014128) {
      if ((int)DAT_08014128 < (int)uVar7) {
        uVar8 = DAT_08014170;
        if (uVar7 == DAT_08014170) {
          uVar8 = FUN_08014a90();
        }
        if ((int)uVar8 < (int)uVar7) {
          uVar8 = DAT_0801418c;
          if (uVar7 == DAT_0801418c) {
            uVar8 = FUN_08014ad4();
          }
          if (uVar7 == uVar8 + 0x10) {
            FUN_08014b68();
          }
          FUN_080152b0();
          return;
        }
        uVar8 = uVar8 - 0x9e;
        if (uVar7 == uVar8) {
          uVar8 = FUN_08014a28();
        }
        if (uVar7 == uVar8 + 0x9c) {
          FUN_08014a4a();
        }
        FUN_080152b0();
        return;
      }
      if (uVar7 != DAT_08014128 - 0x36) {
        if ((int)(DAT_08014128 - 0x36) < (int)uVar7) {
          uVar8 = DAT_08014144;
          if (uVar7 == DAT_08014144) {
            uVar8 = FUN_080149d0();
          }
          if (uVar7 == uVar8 + 0x10) {
            FUN_080149fa();
          }
          FUN_080152b0();
          return;
        }
        uVar8 = DAT_08014128 - 0x77;
        if (uVar7 == uVar8) {
          uVar8 = FUN_080148ec();
        }
        if (uVar7 == uVar8 + 7) {
          FUN_08014950();
        }
        FUN_080152b0();
        return;
      }
      if ((in_stack_00000030 & 1) != 0) {
        iVar6 = 0;
        iVar11 = DAT_080148dc * (1 - in_stack_00000038);
        if ((*(uint *)(iVar11 + DAT_080148d8 + 0x1c) & 0xfffff) >> 0xd != 0) {
          pbVar12 = (byte *)(iVar11 + DAT_080148d8 + DAT_080148e4);
          do {
            bVar1 = *pbVar12;
            if ((bVar1 != 0xff) &&
               ((*(uint *)((*(ushort *)
                             ((bVar1 & 0x7f) * 0x50 + DAT_080148dc * (uint)(bVar1 >> 7) +
                              DAT_080148d8 + 0x24) & 0x7fff) * 4 + iVar3) & 0x1f00000) == 0x100000))
            {
              *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + 500;
            }
            pbVar12 = pbVar12 + 1;
            iVar6 = iVar6 + 1;
          } while (iVar6 < (int)((*(uint *)(DAT_080148dc * (1 - in_stack_00000038) + DAT_080148d8 +
                                           0x1c) & 0xfffff) >> 0xd));
        }
        iVar3 = 0;
        pbVar12 = (byte *)((1 - in_stack_00000038) * 0xb + DAT_080148d8 + DAT_080148e8);
        do {
          bVar1 = *pbVar12;
          if (((bVar1 != 0xff) &&
              (iVar11 = (bVar1 & 0x7f) * 0x50 + (uint)(bVar1 >> 7) * DAT_080148dc + DAT_080148d8,
              (*(byte *)(iVar11 + 0x30) & 0x1f) == 1)) &&
             ((int)((uint)*(byte *)(iVar11 + 0x33) * 0x8000000) < 0)) {
            *(int *)(unaff_r7 + 2) = *(int *)(unaff_r7 + 2) + 500;
          }
          pbVar12 = pbVar12 + 1;
          iVar3 = iVar3 + 1;
        } while (iVar3 < 5);
        FUN_080152b0();
        return;
      }
      FUN_080152b0();
      return;
    }
  }
  if ((in_stack_00000030 & 3) != 0) {
    FUN_0800e158(in_stack_0000002c,0xe);
    return;
  }
  FUN_080152b0();
  return;
}



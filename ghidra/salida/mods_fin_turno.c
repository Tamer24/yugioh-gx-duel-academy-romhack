// ===== 0800EAC4 FUN_0800eac4

undefined4 FUN_0800eac4(uint param_1)

{
  byte bVar1;
  int iVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  byte *pbVar6;
  int iVar7;
  byte *pbVar8;
  int iVar9;
  uint uVar10;
  undefined4 in_lr;
  
  iVar2 = DAT_0800eb04;
  iVar5 = (param_1 & 0x7f) * 0x50 + DAT_0800eb08 * ((param_1 & 0x80) >> 7) + DAT_0800eb04;
  pbVar8 = (byte *)(iVar5 + 0x3c);
  bVar1 = *pbVar8;
  pbVar6 = (byte *)(iVar5 + 0x3d);
  uVar10 = *pbVar6 & 0xf;
  *pbVar8 = 0xff;
  *pbVar6 = 0;
  iVar5 = 0;
  while( true ) {
    iVar9 = (bVar1 & 0x7f) * 0x50;
    iVar7 = (uint)(bVar1 >> 7) * DAT_0800ec10;
    if ((int)(*(byte *)(iVar9 + iVar7 + iVar2 + 0x3e) & 0xf) <= iVar5) {
      return in_lr;
    }
    if (((uint)*(ushort *)(iVar5 * 2 + iVar9 + iVar7 + iVar2 + 0x40) ==
         (param_1 & 0xff | uVar10 << 8)) && (uVar3 = uVar10 - 1, uVar3 < 0xe)) break;
    iVar5 = iVar5 + 1;
  }
                    /* WARNING: Could not recover jumptable at 0x0800eb34. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  uVar4 = (**(code **)(uVar3 * 4 + DAT_0800eb38))();
  return uVar4;
}


// ===== 0800EC14 FUN_0800ec14

undefined4 FUN_0800ec14(uint param_1)

{
  byte bVar1;
  int iVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  byte *pbVar6;
  int iVar7;
  byte *pbVar8;
  int iVar9;
  uint uVar10;
  undefined4 in_lr;
  
  iVar2 = DAT_0800ec54;
  iVar5 = (param_1 & 0x7f) * 0x50 + DAT_0800ec58 * ((param_1 & 0x80) >> 7) + DAT_0800ec54;
  pbVar8 = (byte *)(iVar5 + 0x3c);
  bVar1 = *pbVar8;
  pbVar6 = (byte *)(iVar5 + 0x3d);
  uVar10 = *pbVar6 & 0xf;
  *pbVar8 = 0xff;
  *pbVar6 = 0;
  iVar5 = 0;
  while( true ) {
    iVar9 = (bVar1 & 0x7f) * 0x50;
    iVar7 = (uint)(bVar1 >> 7) * DAT_0800ed64;
    if ((int)(*(byte *)(iVar9 + iVar7 + iVar2 + 0x3e) & 0xf) <= iVar5) {
      return in_lr;
    }
    if (((uint)*(ushort *)(iVar5 * 2 + iVar9 + iVar7 + iVar2 + 0x40) ==
         (param_1 & 0xff | uVar10 << 8)) && (uVar3 = uVar10 - 1, uVar3 < 0xf)) break;
    iVar5 = iVar5 + 1;
  }
                    /* WARNING: Could not recover jumptable at 0x0800ec84. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  uVar4 = (**(code **)(uVar3 * 4 + DAT_0800ec88))();
  return uVar4;
}


// ===== 0800ED68 FUN_0800ed68

/* WARNING: Removing unreachable block (ram,0x0800ee22) */
/* WARNING: Removing unreachable block (ram,0x0800ee6a) */
/* WARNING: Removing unreachable block (ram,0x0800ee8a) */

undefined4 FUN_0800ed68(uint param_1)

{
  uint uVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  undefined4 in_lr;
  
  FUN_0800eac4();
  iVar4 = (param_1 & 0x7f) * 0x50;
  iVar3 = ((param_1 & 0x80) >> 7) * DAT_0800edd8;
  iVar6 = 0;
  iVar5 = DAT_0800edd4;
  if ((*(byte *)(iVar4 + iVar3 + DAT_0800edd4 + 0x3e) & 0xf) != 0) {
    do {
      uVar1 = (*(ushort *)(iVar6 * 2 + iVar4 + iVar3 + iVar5 + 0x40) >> 8 & 0xf) - 1;
      if (uVar1 < 0xf) {
                    /* WARNING: Could not recover jumptable at 0x0800edd2. Too many branches */
                    /* WARNING: Treating indirect jump as call */
        uVar2 = (**(code **)(uVar1 * 4 + DAT_0800eddc))();
        return uVar2;
      }
      iVar6 = iVar6 + 1;
      iVar4 = (param_1 & 0x7f) * 0x50;
      iVar3 = ((param_1 & 0x80) >> 7) * DAT_0800eed4;
      iVar5 = DAT_0800eed0;
    } while (iVar6 < (int)(*(byte *)(iVar4 + iVar3 + DAT_0800eed0 + 0x3e) & 0xf));
  }
  return in_lr;
}


// ===== 0800EED8 FUN_0800eed8

undefined4 FUN_0800eed8(uint param_1)

{
  bool bVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  ushort uVar7;
  byte *pbVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  undefined4 in_lr;
  
  iVar2 = DAT_0800eef4;
  iVar12 = 0;
  do {
    while( true ) {
      iVar9 = (param_1 & 0x7f) * 0x50;
      iVar6 = DAT_0800f04c * ((param_1 & 0x80) >> 7);
      if ((int)(*(byte *)(iVar9 + iVar6 + iVar2 + 0x3e) & 0xf) <= iVar12) {
        return in_lr;
      }
      uVar7 = *(ushort *)(iVar12 * 2 + iVar9 + iVar6 + iVar2 + 0x40);
      uVar4 = (uint)uVar7;
      uVar7 = uVar7 >> 8 & 0xf;
      uVar5 = uVar4 & 0xff;
      bVar1 = false;
      if (uVar7 == 10) break;
      if (10 < uVar7) {
        if ((uVar7 == 0xd) &&
           ((*(uint *)((uVar4 & 0x7f) * 0x50 + DAT_0800f04c * (uVar5 >> 7) + iVar2 + 0x30) & 0xfffff
            ) >> 0x13 == 1 - ((*(byte *)(DAT_0800f004 + iVar2) & 3) >> 1))) {
          bVar1 = true;
        }
        break;
      }
      if (uVar7 != 4) break;
LAB_0800ef64:
      iVar9 = (param_1 & 0x7f) * 0x50;
      iVar10 = DAT_0800f008 * ((param_1 & 0x80) >> 7);
      pbVar8 = (byte *)(iVar9 + iVar10 + iVar2 + 0x3e);
      uVar3 = (*pbVar8 & 0xf) - 1 & 0xf;
      *pbVar8 = *pbVar8 & 0xf0 | (byte)uVar3;
      iVar11 = iVar12 * 2 + 2 + iVar9;
      iVar9 = iVar12 * 2 + iVar9;
      iVar6 = iVar12;
      if (iVar12 < (int)uVar3) {
        do {
          *(undefined2 *)(iVar9 + iVar10 + iVar2 + 0x40) =
               *(undefined2 *)(iVar11 + iVar10 + iVar2 + 0x40);
          iVar11 = iVar11 + 2;
          iVar9 = iVar9 + 2;
          iVar6 = iVar6 + 1;
        } while (iVar6 < (int)(*pbVar8 & 0xf));
      }
      if (uVar5 != 0xff) {
        iVar6 = (uVar4 & 0x7f) * 0x50 + DAT_0800f008 * (uVar5 >> 7) + iVar2;
        pbVar8 = (byte *)(iVar6 + 0x3c);
        if ((uint)*pbVar8 == (param_1 & 0xffff)) {
          *pbVar8 = 0xff;
          *(undefined1 *)(iVar6 + 0x3d) = 0;
        }
      }
    }
    if (bVar1) goto LAB_0800ef64;
    iVar12 = iVar12 + 1;
  } while( true );
}


// ===== 0800F050 FUN_0800f050

undefined4 FUN_0800f050(uint param_1,ushort param_2)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  byte *pbVar10;
  undefined4 in_lr;
  undefined4 local_28;
  
  iVar3 = DAT_0800f074;
  local_28 = 0;
  while( true ) {
    iVar8 = (param_1 & 0x7f) * 0x50;
    iVar9 = DAT_0800f170 * ((param_1 & 0x80) >> 7);
    pbVar10 = (byte *)(iVar8 + iVar9 + iVar3 + 0x3e);
    bVar1 = *pbVar10;
    if ((int)(bVar1 & 0xf) <= local_28) break;
    iVar4 = local_28 * 2 + iVar8;
    uVar2 = *(ushort *)(iVar4 + iVar9 + iVar3 + 0x40);
    uVar6 = uVar2 & 0xff;
    if ((uVar2 >> 8 & 0xf) == param_2) {
      uVar5 = (bVar1 & 0xf) - 1 & 0xf;
      *pbVar10 = bVar1 & 0xf0 | (byte)uVar5;
      iVar8 = local_28 * 2 + 2 + iVar8;
      iVar7 = local_28;
      if (local_28 < (int)uVar5) {
        do {
          *(undefined2 *)(iVar4 + iVar9 + iVar3 + 0x40) =
               *(undefined2 *)(iVar8 + iVar9 + iVar3 + 0x40);
          iVar8 = iVar8 + 2;
          iVar4 = iVar4 + 2;
          iVar7 = iVar7 + 1;
        } while (iVar7 < (int)(*pbVar10 & 0xf));
      }
      if (uVar6 != 0xff) {
        iVar8 = (uVar2 & 0x7f) * 0x50 + DAT_0800f120 * (uVar6 >> 7) + iVar3;
        pbVar10 = (byte *)(iVar8 + 0x3c);
        if ((uint)*pbVar10 == (param_1 & 0xffff)) {
          *pbVar10 = 0xff;
          *(undefined1 *)(iVar8 + 0x3d) = 0;
        }
      }
    }
    else {
      local_28 = local_28 + 1;
    }
  }
  return in_lr;
}


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
                    /* WARNING: Subroutine does not return */
                FUN_0800e158(param_2,0xe);
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


// ===== 0801FC5C FUN_0801fc5c

longlong FUN_0801fc5c(uint param_1)

{
  byte bVar1;
  ushort uVar2;
  short sVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  uint uVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  uint in_lr;
  
  iVar7 = DAT_0801fd4c;
  iVar4 = (int)(param_1 & 0x80) >> 7;
  uVar5 = param_1 & 0x7f;
  iVar10 = uVar5 * 0x50 + DAT_0801fd50 * iVar4 + DAT_0801fd4c;
  uVar2 = *(ushort *)(iVar10 + 0x24);
  uVar8 = *(uint *)(iVar10 + 0x30) & 0xfffff;
  uVar6 = uVar8 >> 0x13;
  bVar1 = *(byte *)(iVar10 + 0x33);
  if (((*(char *)(DAT_0801fd50 * uVar6 + DAT_0801fd4c + DAT_0801fd50 + -0x18) < '\0') ||
      ((((uVar5 - 100 < 0x1b && ((uVar2 & 0x7fff) == 0xd)) || ((uVar8 >> 0xc & 0x7f) != 0)) ||
       ((uVar6 != (*(byte *)(DAT_0801fd4c + DAT_0801fd54) & 3) >> 1 || ((bVar1 & 0x1f) >> 4 == 0))))
      )) || (sVar3 = FUN_0800e09c(iVar4,uVar5,0xc), sVar3 != 0)) goto LAB_0801fd6c;
  iVar10 = (uVar2 & 0x7fff) * 2;
  uVar8 = (uint)*(ushort *)(iVar10 + DAT_0801fd58);
  if (uVar8 == DAT_0801fd5c) {
    iVar7 = (uint)*(byte *)(DAT_0801fea8 * uVar6 + iVar7 + DAT_0801feac) << 0x1a;
LAB_0801fda6:
    if (iVar7 < 0) goto LAB_0801fd6c;
LAB_0801fdaa:
    if ((bVar1 & 0x3f) >> 5 != 0) goto LAB_0801fd6c;
  }
  else {
    if ((int)uVar8 <= (int)DAT_0801fd5c) {
      if (uVar8 == DAT_0801fd5c - 0x51) {
        iVar7 = (uint)*(byte *)(DAT_0801fd8c * uVar6 + iVar7 + DAT_0801fd90) << 0x1c;
        goto LAB_0801fda6;
      }
      goto LAB_0801fdaa;
    }
    if (uVar8 != DAT_0801fd70) {
      if (uVar8 == DAT_0801fd74) goto LAB_0801fd6c;
      goto LAB_0801fdaa;
    }
  }
  sVar3 = FUN_0800e09c(iVar4,uVar5,0xb);
  if (((sVar3 == 0) && (sVar3 = FUN_0800e09c(iVar4,uVar5,0x18), sVar3 == 0)) &&
     (sVar3 = FUN_0800e09c(iVar4,uVar5,0x19), sVar3 == 0)) {
    iVar4 = (param_1 & 0x7f) * 0x50;
    iVar7 = iVar4 + DAT_0801fea8 * ((int)(param_1 & 0x80) >> 7) + DAT_0801feb0;
    if ((*(byte *)(iVar7 + 0x34) & 0x1f) >> 2 == 0) {
      iVar11 = 0;
      iVar9 = iVar4;
      if ((*(byte *)(iVar7 + 0x3e) & 0xf) != 0) {
        do {
          uVar8 = (uint)*(byte *)(iVar9 + DAT_0801fea8 * ((int)(param_1 & 0x80) >> 7) +
                                 DAT_0801feb0 + 0x40);
          if ((int)((uint)*(byte *)((uVar8 & 0x7f) * 0x50 +
                                    DAT_0801fea8 * ((int)(uVar8 & 0x80) >> 7) + DAT_0801feb0 + 0x33)
                   * 0x8000000) < 0) {
                    /* WARNING: Subroutine does not return */
            FUN_0800e158(uVar8,0x1f);
          }
          iVar9 = iVar9 + 2;
          iVar11 = iVar11 + 1;
        } while (iVar11 < (int)(*(byte *)(DAT_0801ffd8 * ((int)(param_1 & 0x80) >> 7) + iVar4 +
                                          DAT_0801ffdc + 0x3e) & 0xf));
      }
      iVar7 = 0;
      do {
        iVar4 = 0;
        do {
          bVar1 = *(byte *)(iVar4 + iVar7 * 0xb + DAT_0801ffe0 + DAT_0801ffdc);
          uVar8 = (uint)bVar1;
          if ((uVar8 != 0xff) &&
             ((int)((uint)*(byte *)((uVar8 & 0x7f) * 0x50 + DAT_0801ffd8 * (uint)(bVar1 >> 7) +
                                    DAT_0801ffdc + 0x33) * 0x8000000) < 0)) {
                    /* WARNING: Subroutine does not return */
            FUN_0800e158(uVar8,0x1f);
          }
          iVar4 = iVar4 + 1;
        } while (iVar4 < 0xb);
        iVar7 = iVar7 + 1;
      } while (iVar7 < 2);
      uVar8 = (uint)*(ushort *)(iVar10 + DAT_080200d0);
      if (uVar8 == DAT_080200d4) {
        iVar7 = FUN_08010bec(1 - uVar6);
        if (iVar7 != 0) goto LAB_080200f6;
      }
      else if ((uVar8 != DAT_080200d4 + 0x5e) || (iVar7 = FUN_08010d64(uVar6,1), 1 < iVar7)) {
LAB_080200f6:
                    /* WARNING: Subroutine does not return */
        FUN_0800e158(param_1,0xd);
      }
    }
  }
LAB_0801fd6c:
  return (ulonglong)in_lr << 0x20;
}



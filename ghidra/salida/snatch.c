// ===== 0803F2E8 FUN_0803f2e8

longlong FUN_0803f2e8(uint *param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  uint in_lr;
  longlong lVar5;
  
  iVar2 = DAT_0803f3f4;
  iVar1 = DAT_0803f3f0;
  uVar4 = (uint)(ushort)*param_1;
  if (((*(uint *)(((uVar4 & 0x1ff) >> 1 & 0x7f) * 0x50 + ((uVar4 & 0x1ff) >> 8) * DAT_0803f3f4 +
                  DAT_0803f3f0 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 5) {
    if ((*param_1 & DAT_0803f3f8) == 0x4c00) {
      lVar5 = FUN_0800e158((uVar4 & 0x1ff) >> 1,0x1f);
      return lVar5;
    }
    if ((param_1[2] & 0xf) == 1) {
      uVar4 = (uint)*(byte *)((int)param_1 + 9);
      iVar3 = FUN_080616b8(param_1,uVar4);
      if (iVar3 == 0) {
        uVar4 = ((ushort)*param_1 & 0x1ff) >> 1;
        FUN_080184c0((byte)*param_1 & 1,uVar4,uVar4);
      }
      else {
        FUN_0801a600((byte)*param_1 & 1,((ushort)*param_1 & 0x1ff) >> 1,uVar4);
        if ((*(ushort *)
              ((*(ushort *)
                 ((uVar4 & 0x7f) * 0x50 + ((int)(uVar4 & 0x80) >> 7) * iVar2 + iVar1 + 0x24) &
               0x7fff) * 2 + DAT_0803f498) != DAT_0803f49c) && ((*param_1 & 0x80000) == 0)) {
          lVar5 = FUN_0800e158(((ushort)*param_1 & 0x1ff) >> 1,0x1f);
          return lVar5;
        }
      }
    }
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 08033254 FUN_08033254

undefined8 FUN_08033254(uint *param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 in_lr;
  
  if (((*param_1 & DAT_08033278) == 0x4c00) ||
     (iVar1 = count_empty_field_slots((byte)*param_1 & 1), iVar1 != 0)) {
    uVar2 = 1;
  }
  else {
    uVar2 = 0;
  }
  return CONCAT44(in_lr,uVar2);
}


// ===== 0802A750 FUN_0802a750

undefined8 FUN_0802a750(uint *param_1,uint param_2)

{
  uint uVar1;
  int iVar2;
  undefined4 in_lr;
  
  if ((*param_1 & DAT_0802a76c) == 0x4c00) {
    uVar1 = 1;
  }
  else {
    iVar2 = (param_2 & 0x7f) * 0x50 + DAT_0802a7c0 * ((param_2 & 0x80) >> 7) + DAT_0802a7bc;
    uVar1 = *(uint *)(iVar2 + 0x30);
    if ((((uVar1 & 0xfffff) >> 0xc & 0x7f) == 0) &&
       ((uVar1 & 0xfffff) >> 0x13 != ((byte)*param_1 & 1))) {
      uVar1 = (*(byte *)(iVar2 + 0x33) & 0x1f) >> 4;
    }
    else {
      uVar1 = 0;
    }
  }
  return CONCAT44(in_lr,uVar1);
}


// ===== 0801A8A4 FUN_0801a8a4

undefined8 FUN_0801a8a4(uint param_1)

{
  short sVar1;
  uint uVar2;
  uint uVar3;
  undefined4 uVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  undefined4 in_lr;
  
  uVar8 = param_1 & 0xffff;
  uVar9 = (param_1 & 0x80) >> 7;
  iVar6 = (param_1 & 0x7f) * 0x50 + uVar9 * DAT_0801a930 + DAT_0801a92c;
  uVar3 = *(uint *)(iVar6 + 0x30) & 0xfffff;
  uVar5 = uVar3 >> 0x13;
  uVar2 = FUN_08011074(1 - uVar5);
  if (((uVar8 != 0xff) && ((uVar3 >> 0xc & 0x7f) == 0)) && (uVar2 != 0xffffffff)) {
    if ((*(ushort *)((*(ushort *)(iVar6 + 0x24) & 0x7fff) * 2 + DAT_0801a934) != DAT_0801a938) ||
       (-1 < (int)((uint)*(byte *)(iVar6 + 0x33) * 0x8000000))) {
      uVar3 = param_1 & 0x7f;
      uVar7 = (param_1 & 0x80) >> 7;
      iVar6 = uVar3 * 0x50 + uVar7 * DAT_0801a9b0 + DAT_0801a9ac;
      uVar9 = (uint)*(byte *)(iVar6 + 0x33);
      FUN_080188ac(uVar8,(1 - uVar5 & 1) << 0xf | (uVar2 & 0x3f) << 4 | ((uVar9 & 0x1f) >> 4) << 3 |
                         ((uVar9 & 0x3f) >> 5) << 2);
      if ((uVar3 - 100 & 0xffff) < 0x1b) {
        iVar6 = 1 << (uVar2 & 0xff);
      }
      else {
        uVar9 = (uint)*(ushort *)((*(ushort *)(iVar6 + 0x24) & 0x7fff) * 2 + DAT_0801a9d0);
        if (uVar9 == DAT_0801a9d4) {
          sVar1 = FUN_0800e09c(uVar7,uVar3,0xe);
          if (sVar1 == 0) {
            FUN_0801aa84(uVar7,uVar8);
            uVar4 = 0x3c;
            if (uVar5 != 0) {
              uVar4 = DAT_0801aa10;
            }
            drawing_FUN_08022034(uVar4,uVar8,0xe);
            FUN_0801abf0(1 - uVar5,2000);
          }
        }
        else if ((uVar9 == DAT_0801a9d4 + 0x3f) &&
                (sVar1 = FUN_0800e09c(uVar7,uVar3,0xe), sVar1 == 0)) {
          FUN_0801aa84(uVar7,uVar8);
          uVar4 = 0x3c;
          if (uVar5 != 0) {
            uVar4 = DAT_0801aa5c;
          }
          drawing_FUN_08022034(uVar4,uVar8,0xe);
          FUN_0801abf0(uVar5,DAT_0801aa60);
        }
        iVar6 = 1 << (uVar2 & 0xff);
      }
      goto LAB_0801aa4c;
    }
    FUN_0801aa84(uVar9,uVar8);
  }
  iVar6 = 0;
LAB_0801aa4c:
  return CONCAT44(in_lr,iVar6);
}


// ===== 08052BE0 FUN_08052be0

undefined8 FUN_08052be0(uint *param_1)

{
  char cVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  undefined4 uVar5;
  uint uVar6;
  undefined4 in_r12;
  undefined4 in_lr;
  undefined8 uVar7;
  
  if ((*param_1 & DAT_08052c28) != 0x4c00) {
    uVar6 = (uint)(byte)*param_1;
    if (((byte)*param_1 & 1) == 0) {
      if ((*(uint *)(DAT_08052c90 + 0x7c0) & 0x3ffff) >> 10 != 0) {
        uVar6 = (uint)*(ushort *)
                       ((*(ushort *)
                          ((((ushort)*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_08052dc4 * (((ushort)*param_1 & 0x1ff) >> 8) + DAT_08052dc0 + 0x24) &
                        0x7fff) * 2 + DAT_08052dbc);
        if (uVar6 == DAT_08052dc8) {
LAB_08052e00:
          in_r12 = 0xe00000;
        }
        else {
          if ((int)DAT_08052dc8 < (int)uVar6) {
            if (uVar6 == DAT_08052de8) goto LAB_08052e00;
            uVar4 = DAT_08052dfc;
            if ((int)uVar6 <= (int)DAT_08052de8) {
              uVar4 = DAT_08052de8 - 0xbb;
            }
          }
          else {
            if (uVar6 == DAT_08052dc8 - 0xdf) goto LAB_08052e00;
            uVar4 = DAT_08052dd0;
            if ((int)uVar6 <= (int)(DAT_08052dc8 - 0xdf)) {
              uVar4 = DAT_08052dc8 - 0xfb;
            }
          }
          if (uVar6 == uVar4) {
            in_r12 = 0xf00000;
          }
        }
        iVar2 = FUN_08009094(in_r12);
        if (iVar2 != 0) {
          cVar1 = *(char *)(DAT_08052e3c + DAT_08052e40);
          if ((((*DAT_08052e44 & 1) == 0) || (*(short *)(DAT_08052e48 + DAT_08052e4c) != 0x50)) ||
             (cVar1 == -0x7d)) {
            iVar2 = FUN_080616b8(param_1,cVar1);
            if ((iVar2 != 0) && (iVar2 = FUN_08051680(param_1,cVar1), iVar2 != 0))
            goto LAB_08052e68;
            FUN_080e6d88(3);
          }
          else {
            FUN_080e6d88(3);
          }
        }
        uVar5 = 0;
        goto LAB_08052e74;
      }
      *(byte *)(param_1 + 2) = (byte)param_1[2] & 0xf0;
      uVar4 = (uint)*(ushort *)
                     ((*(ushort *)
                        ((((ushort)*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         DAT_08052c9c * (((ushort)*param_1 & 0x1ff) >> 8) + DAT_08052c98 + 0x24) &
                      0x7fff) * 2 + DAT_08052c94);
      if (uVar4 == DAT_08052ca0) {
LAB_08052d08:
        iVar2 = FUN_08010c10(1 - (uVar6 & 1),1,0);
        if (iVar2 != 0) {
          uVar7 = ask_question(DAT_08052d28);
          return uVar7;
        }
      }
      else {
        if ((int)DAT_08052ca0 < (int)uVar4) {
          if (uVar4 == DAT_08052cb4) goto LAB_08052d08;
          uVar3 = DAT_08052cc0;
          if ((int)uVar4 <= (int)DAT_08052cb4) {
            uVar3 = DAT_08052cb4 - 0xbb;
          }
        }
        else {
          if (uVar4 == DAT_08052ca0 - 0xfb) {
            iVar2 = FUN_08010c10(1 - (uVar6 & 1),0,0);
            if (iVar2 != 0) {
              uVar7 = ask_question(DAT_08052ce0);
              return uVar7;
            }
            goto LAB_08052e68;
          }
          uVar3 = DAT_08052ca0 - 0x26;
        }
        if (uVar4 == uVar3) {
          iVar2 = FUN_08010c10(1 - (uVar6 & 1),0,0);
          if (iVar2 != 0) {
            uVar7 = ask_question(DAT_08052d04);
            return uVar7;
          }
        }
        else {
          iVar2 = FUN_08010c10(1 - (uVar6 & 1),0,0);
          if (iVar2 != 0) {
            uVar7 = ask_question(DAT_08052d68);
            return uVar7;
          }
        }
      }
    }
    else {
      iVar2 = FUN_08072d44(param_1,1,0xffffffff);
      *(byte *)(param_1 + 2) = (byte)param_1[2] & 0xf0;
      if (iVar2 != 0xff) {
        FUN_08051680(param_1);
      }
    }
  }
LAB_08052e68:
  uVar5 = 1;
LAB_08052e74:
  return CONCAT44(in_lr,uVar5);
}



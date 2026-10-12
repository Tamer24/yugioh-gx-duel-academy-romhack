// ===== 08041E84 FUN_08041e84

longlong FUN_08041e84(byte *param_1)

{
  byte bVar1;
  byte bVar2;
  int iVar3;
  undefined4 uVar4;
  uint in_lr;
  
  if (((param_1[2] & 8) == 0) && ((param_1[8] & 0xf) == 2)) {
    bVar1 = param_1[9];
    bVar2 = param_1[10];
    iVar3 = FUN_0800e874(bVar1,0);
    if ((iVar3 != 0) &&
       (((iVar3 = FUN_0800e888(bVar1,0), iVar3 != 0 && (iVar3 = FUN_0800e874(bVar2,0), iVar3 != 0))
        && (iVar3 = FUN_0800e888(bVar2,0), iVar3 != 0)))) {
      bVar2 = *param_1;
      FUN_080159e0(bVar1,0);
      uVar4 = FUN_080e22ec();
      FUN_0801a5bc(-((int)((uint)bVar2 << 0x1f) >> 0x1f),uVar4,param_1[10],9);
    }
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 0802A7CC FUN_0802a7cc

undefined8 FUN_0802a7cc(ushort *param_1,uint param_2)

{
  uint uVar1;
  undefined4 uVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  undefined4 in_lr;
  
  if ((param_2 & 0xffff) != 0xff) {
    iVar4 = (param_2 & 0x7f) * 0x50 + DAT_0802a87c * ((param_2 & 0x80) >> 7) + DAT_0802a878;
    uVar1 = *(uint *)(iVar4 + 0x30);
    if ((((uVar1 & 0xfffff) >> 0xc & 0x7f) == 0) &&
       ((int)((uint)*(byte *)(iVar4 + 0x33) * 0x8000000) < 0)) {
      uVar5 = (uint)*param_1;
      uVar3 = (uint)*(ushort *)
                     ((*(ushort *)
                        (((uVar5 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         DAT_0802a87c * ((uVar5 & 0x1ff) >> 8) + DAT_0802a878 + 0x24) & 0x7fff) * 2
                     + DAT_0802a880);
      if (uVar3 == DAT_0802a884) {
        if ((param_2 & 0xffff) != (uVar5 & 0x1ff) >> 1) goto LAB_0802a892;
      }
      else if ((uVar3 != DAT_0802a888) || ((uVar1 & 0xfffff) >> 0x13 == ((byte)*param_1 & 1))) {
LAB_0802a892:
        uVar2 = 1;
        goto LAB_0802a894;
      }
    }
  }
  uVar2 = 0;
LAB_0802a894:
  return CONCAT44(in_lr,uVar2);
}


// ===== 08033D7C FUN_08033d7c

undefined8 FUN_08033d7c(void)

{
  int iVar1;
  int iVar2;
  undefined4 in_lr;
  
  iVar1 = FUN_08010c10(0,1,0);
  iVar2 = FUN_08010c10(1,1,0);
  return CONCAT44(in_lr,(uint)(1 < iVar1 + iVar2));
}


// ===== 0805425C FUN_0805425c

undefined8 FUN_0805425c(int param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 uVar3;
  uint *puVar4;
  undefined4 in_lr;
  
  puVar4 = (uint *)(DAT_0805427c + 0x7c0);
  uVar1 = (*puVar4 & 0x3ffff) >> 10;
  if (uVar1 == 1) {
    if ((*(ushort *)(DAT_080542d4 + 0x148) & 2) == 0) {
      iVar2 = FUN_08009094(DAT_080542d8);
      if (iVar2 != 0) {
        FUN_08051680(param_1,*(undefined1 *)(DAT_080542dc + DAT_080542e0));
        *puVar4 = DAT_08054308 & *puVar4 | (((*puVar4 & 0x3ffff) >> 10) + 1 & 0xff) << 10;
      }
      goto LAB_08054300;
    }
LAB_0805431e:
    *puVar4 = *puVar4 & DAT_0805432c;
    goto LAB_08054300;
  }
  if (uVar1 < 2) {
    if (uVar1 == 0) {
      *(byte *)(param_1 + 8) = *(byte *)(param_1 + 8) & 0xf0;
      iVar2 = FUN_08033d7c(param_1,0);
      uVar3 = DAT_080542a4;
      if (iVar2 != 0) goto LAB_080542e6;
    }
  }
  else {
    uVar3 = DAT_08054304;
    if (uVar1 == 2) {
LAB_080542e6:
                    /* WARNING: Subroutine does not return */
      ask_question(uVar3);
    }
    if (uVar1 == 3) {
      if ((*(ushort *)(DAT_08054328 + 0x148) & 2) != 0) goto LAB_0805431e;
      iVar2 = FUN_08009094(DAT_08054350);
      if (iVar2 != 0) {
        if (*(char *)(param_1 + 9) != *(char *)(DAT_08054354 + DAT_08054358)) {
          FUN_08051680(param_1);
          goto LAB_08054362;
        }
        FUN_080e6d88(3);
      }
LAB_08054300:
      uVar3 = 0;
      goto LAB_08054364;
    }
  }
LAB_08054362:
  uVar3 = 1;
LAB_08054364:
  return CONCAT44(in_lr,uVar3);
}


// ===== 0803EB98 FUN_0803eb98

longlong FUN_0803eb98(ushort *param_1)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  uint uVar4;
  uint in_lr;
  
  iVar1 = DAT_0803ec34;
  if ((param_1[1] & 8) == 0) {
    if ((param_1[4] & 0xf) == 1) {
      iVar2 = FUN_0806149c(*(byte *)((int)param_1 + 9));
      if ((iVar2 == 0) && (iVar2 = FUN_0801a8a4(*(byte *)((int)param_1 + 9),0), iVar2 != 0)) {
        uVar3 = 0x3b;
        if ((*param_1 & 1) != 0) {
          uVar3 = DAT_0803ec38;
        }
        drawing_FUN_08022034(uVar3,*(byte *)((int)param_1 + 9),0x15);
        FUN_0801a5bc((byte)*param_1 & 1,(*param_1 & 0x1ff) >> 1,*(byte *)((int)param_1 + 9),4);
        uVar4 = (uint)*param_1;
        if (*(ushort *)
             ((*(ushort *)
                (((uVar4 & 0x1ff) >> 1 & 0x7f) * 0x50 + DAT_0803ec40 * ((uVar4 & 0x1ff) >> 8) +
                 iVar1 + 0x24) & 0x7fff) * 2 + DAT_0803ec3c) == DAT_0803ec44) {
          FUN_08018850((uVar4 & 0x1ff) >> 1);
        }
      }
    }
  }
  return (ulonglong)in_lr << 0x20;
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
                    /* WARNING: Subroutine does not return */
          ask_question(DAT_08052d28);
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
                    /* WARNING: Subroutine does not return */
              ask_question(DAT_08052ce0);
            }
            goto LAB_08052e68;
          }
          uVar3 = DAT_08052ca0 - 0x26;
        }
        if (uVar4 == uVar3) {
          iVar2 = FUN_08010c10(1 - (uVar6 & 1),0,0);
          if (iVar2 != 0) {
                    /* WARNING: Subroutine does not return */
            ask_question(DAT_08052d04);
          }
        }
        else {
          iVar2 = FUN_08010c10(1 - (uVar6 & 1),0,0);
          if (iVar2 != 0) {
                    /* WARNING: Subroutine does not return */
            ask_question(DAT_08052d68);
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



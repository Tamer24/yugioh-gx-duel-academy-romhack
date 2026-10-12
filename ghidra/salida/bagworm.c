// ===== 08042174 FUN_08042174

longlong FUN_08042174(ushort *param_1)

{
  byte bVar1;
  short sVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  uint in_lr;
  
  if (((param_1[1] & 8) == 0) && ((param_1[4] & 0xf) == 1)) {
    bVar1 = *(byte *)((int)param_1 + 9);
    uVar3 = FUN_08011074((byte)*param_1 & 1,0);
    if (((bVar1 != ((byte)*param_1 & 1)) &&
        (((iVar4 = FUN_0800e874(bVar1,0), iVar4 != 0 && (iVar4 = FUN_0800e888(bVar1,0), iVar4 != 0))
         && (uVar3 != 0xffffffff)))) && (sVar2 = FUN_08015a08(bVar1,0), sVar2 == 7)) {
      uVar5 = -((int)((uint)(byte)*param_1 << 0x1f) >> 0x1f);
      FUN_0801a5bc(uVar5,*(ushort *)
                          (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_08042224 * ((*param_1 & 0x1ff) >> 8) + DAT_08042220 + 0x24) & 0x7fff,
                   (uVar3 & 0xff) << 8 | uVar5,4);
    }
  }
  return (ulonglong)in_lr << 0x20;
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


// ===== 0800E9B8 FUN_0800e9b8

undefined4 FUN_0800e9b8(undefined4 param_1,undefined1 param_2,uint param_3,uint param_4)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  undefined2 *puVar5;
  undefined1 uVar6;
  int iVar7;
  byte *pbVar8;
  int iVar9;
  undefined4 in_lr;
  
  iVar7 = DAT_0800ea48;
  iVar1 = DAT_0800ea44;
  uVar6 = (undefined1)param_3;
  iVar2 = (param_3 & 0x7f) * 0x50;
  iVar9 = DAT_0800ea48 * ((param_3 & 0x80) >> 7);
  iVar3 = iVar2 + iVar9 + DAT_0800ea44;
  *(char *)(iVar3 + 0x3c) = (char)param_4;
  *(undefined1 *)(iVar3 + 0x3d) = param_2;
  uVar4 = (uint)*(ushort *)((*(ushort *)(iVar3 + 0x24) & 0x7fff) * 2 + DAT_0800ea4c);
  if ((uVar4 == DAT_0800ea50) || (uVar4 == DAT_0800ea54)) {
    pbVar8 = (byte *)(iVar3 + 0x3e);
    if (0xf < (*pbVar8 & 0xf)) {
      return in_lr;
    }
    puVar5 = (undefined2 *)((*pbVar8 & 0xf) * 2 + iVar2 + iVar9 + iVar1 + 0x40);
    uVar6 = (char)param_4;
  }
  else {
    iVar2 = (param_4 & 0x7f) * 0x50;
    iVar7 = iVar7 * ((param_4 & 0x80) >> 7);
    pbVar8 = (byte *)(iVar2 + iVar7 + iVar1 + 0x3e);
    if (0xf < (*pbVar8 & 0xf)) {
      return in_lr;
    }
    puVar5 = (undefined2 *)((*pbVar8 & 0xf) * 2 + iVar2 + iVar7 + iVar1 + 0x40);
  }
  *puVar5 = CONCAT11(param_2,uVar6);
  *pbVar8 = *pbVar8 & 0xf0 | (*pbVar8 & 0xf) + 1 & 0xf;
  return in_lr;
}



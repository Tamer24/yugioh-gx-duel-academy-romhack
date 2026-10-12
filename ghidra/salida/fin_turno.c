// ===== 0801D7DC FUN_0801d7dc

undefined4 FUN_0801d7dc(void)

{
  byte bVar1;
  char cVar2;
  ushort uVar3;
  undefined4 uVar4;
  uint uVar5;
  ushort *puVar6;
  byte *pbVar7;
  uint uVar8;
  int iVar9;
  undefined1 *puVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  int iVar16;
  undefined4 in_lr;
  
  iVar16 = DAT_0801db64;
  uVar3 = *DAT_0801db60;
  *(byte *)(DAT_0801db64 + DAT_0801db68) = *(byte *)(DAT_0801db64 + DAT_0801db68) & 0xe3 | 0x18;
  iVar9 = DAT_0801db6c * (uint)(uVar3 >> 0xf);
  puVar6 = (ushort *)(iVar9 + iVar16 + DAT_0801db70);
  *puVar6 = (ushort)DAT_0801db74 & *puVar6;
  puVar10 = (undefined1 *)(iVar9 + iVar16 + DAT_0801db78);
  iVar16 = 0x3f;
  do {
    *puVar10 = 0xff;
    puVar10 = puVar10 + 1;
    iVar16 = iVar16 + -1;
  } while (-1 < iVar16);
  iVar16 = DAT_0801db6c * (uint)(uVar3 >> 0xf) + DAT_0801db64;
  pbVar7 = (byte *)(iVar16 + DAT_0801db7c);
  *pbVar7 = *pbVar7 & 0xfd;
  pbVar7 = (byte *)(iVar16 + DAT_0801db80);
  *pbVar7 = *pbVar7 & 0xf7;
  iVar16 = 0;
  do {
    iVar9 = DAT_0801db64;
    iVar13 = DAT_0801db6c * iVar16 + DAT_0801db64;
    *(byte *)(iVar13 + DAT_0801db84) = *(byte *)(iVar13 + DAT_0801db84) & 0x87;
    pbVar7 = (byte *)(iVar13 + DAT_0801db88);
    if ((int)((uint)*pbVar7 * 0x40000000) < 0) {
      bVar1 = *(byte *)(iVar13 + DAT_0801db8c);
      uVar8 = ((*pbVar7 & 1) << 4 | (uint)(bVar1 >> 4)) + 1;
      *(byte *)(iVar13 + DAT_0801db8c) = bVar1 & 0xf | (byte)((uVar8 & 0xf) << 4);
      *pbVar7 = *pbVar7 & 0xfe | (byte)(uVar8 >> 4) & 1;
    }
    *(byte *)(iVar13 + DAT_0801db7c) = *(byte *)(iVar13 + DAT_0801db7c) & 0xbf;
    puVar6 = (ushort *)(iVar13 + DAT_0801db90);
    *(byte *)puVar6 = (byte)*puVar6 & 0xbf;
    *puVar6 = (ushort)DAT_0801db94 & *puVar6;
    *pbVar7 = *pbVar7 & 0x3f;
    *(byte *)(iVar13 + DAT_0801db80) = *(byte *)(iVar13 + DAT_0801db80) & 0xef;
    iVar15 = DAT_0801dba4;
    iVar13 = DAT_0801db64;
    iVar14 = 0;
    iVar11 = iVar16 + 1;
    do {
      cVar2 = *(char *)(iVar14 + iVar16 * 0xb + DAT_0801db9c + iVar9);
      if (cVar2 != -1) {
        FUN_0800e194(cVar2,5);
        FUN_0800e194(cVar2,6);
        FUN_0800e194(cVar2,0x19);
        uVar4 = FUN_0800e158(cVar2,0x18);
        return uVar4;
      }
      iVar14 = iVar14 + 1;
    } while (iVar14 < 5);
    iVar9 = 5;
    do {
      bVar1 = *(byte *)(iVar9 + iVar16 * 0xb + iVar13 + DAT_0801db9c);
      uVar8 = (uint)bVar1;
      if (uVar8 != 0xff) {
        FUN_0800e194(uVar8,5);
        FUN_0800e194(uVar8,6);
        iVar14 = (uVar8 & 0x7f) * 0x50 + DAT_0801db6c * (uint)(bVar1 >> 7) + iVar13;
        uVar5 = (*(uint *)((*(ushort *)(iVar14 + 0x24) & 0x7fff) * 4 + iVar15) & 0x1f00000) >> 0x14;
        if (((uVar5 < 0x17) && (0x14 < uVar5)) &&
           (-1 < (int)((uint)*(byte *)(iVar14 + 0x33) * 0x8000000))) {
          uVar4 = FUN_0800e158(uVar8,0x1e);
          return uVar4;
        }
      }
      iVar14 = DAT_0801db64;
      iVar9 = iVar9 + 1;
    } while (iVar9 < 0xb);
    iVar13 = 0;
    iVar9 = DAT_0801db6c * iVar16 + DAT_0801db64;
    if ((*(byte *)(iVar9 + 0x1c) & 0x3f) != 0 || *(char *)(iVar9 + 0x1b) < '\0') {
      iVar15 = DAT_0801db6c * iVar16;
      iVar9 = iVar15 + DAT_0801db64;
      do {
        cVar2 = *(char *)(iVar13 + iVar15 + DAT_0801dba8 + iVar14);
        if (cVar2 != -1) {
          FUN_0800e194(cVar2,5);
          FUN_0800e194(cVar2,6);
        }
        iVar13 = iVar13 + 1;
      } while (iVar13 < (int)((*(byte *)(iVar9 + 0x1c) & 0x3f) << 1 |
                             (uint)(*(byte *)(iVar9 + 0x1b) >> 7)));
    }
    iVar9 = DAT_0801db64;
    iVar13 = 0;
    if ((*(ushort *)(DAT_0801db6c * iVar16 + iVar14 + 0x1c) & 0x1fff) >> 6 != 0) {
      iVar12 = DAT_0801db6c * iVar16;
      iVar15 = iVar12 + DAT_0801db64;
      do {
        cVar2 = *(char *)(iVar13 + iVar12 + iVar9 + DAT_0801dbac);
        if (cVar2 != -1) {
          FUN_0800e194(cVar2,5);
          FUN_0800e194(cVar2,6);
        }
        iVar13 = iVar13 + 1;
        iVar14 = iVar9;
      } while (iVar13 < (int)((*(ushort *)(iVar15 + 0x1c) & 0x1fff) >> 6));
    }
    iVar9 = DAT_0801db64;
    iVar13 = 0;
    if ((*(uint *)(DAT_0801db6c * iVar16 + iVar14 + 0x1c) & 0xfffff) >> 0xd != 0) {
      iVar16 = DAT_0801db6c * iVar16;
      iVar15 = iVar16 + DAT_0801db64;
      do {
        cVar2 = *(char *)(iVar13 + iVar16 + DAT_0801dbb0 + iVar9);
        if (cVar2 != -1) {
          FUN_0800e194(cVar2,5);
          FUN_0800e194(cVar2,6);
        }
        iVar13 = iVar13 + 1;
      } while (iVar13 < (int)((*(uint *)(iVar15 + 0x1c) & 0xfffff) >> 0xd));
    }
    iVar16 = iVar11;
  } while (iVar11 < 2);
  *(byte *)(DAT_0801db60 + 0x488) = (byte)DAT_0801db60[0x488] & 0xdf;
  return in_lr;
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



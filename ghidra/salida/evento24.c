// ===== 0801C9B0 FUN_0801c9b0

undefined4 FUN_0801c9b0(void)

{
  ushort *puVar1;
  byte bVar2;
  uint uVar3;
  byte *pbVar4;
  undefined4 in_lr;
  
  puVar1 = DAT_0801c9d4;
  uVar3 = (uint)(*DAT_0801c9d4 >> 0xf);
  pbVar4 = (byte *)((int)DAT_0801c9d4 + DAT_0801c9d8);
  bVar2 = *pbVar4 & 0x7f;
  if (bVar2 == 1) {
    if (((*(byte *)(DAT_0801caa4 + 0x208) & 8) != 0) &&
       ((*(byte *)(DAT_0801caa8 + DAT_0801caac) & 2) == 0)) {
      FUN_08027140(uVar3);
      *pbVar4 = *pbVar4 & 0x80 | 10;
      return in_lr;
    }
    bVar2 = (byte)DAT_0801c9d4[0x488] & 0xdf;
  }
  else {
    if (bVar2 < 2) {
      if (((*pbVar4 & 0x7f) == 0) &&
         ((*(ushort *)(uVar3 * DAT_0801ca54 + DAT_0801ca50 + 0x1c) & 0x1fff) >> 6 != 0)) {
        *(uint *)((int)DAT_0801c9d4 + DAT_0801ca58) =
             *(uint *)((int)DAT_0801c9d4 + DAT_0801ca58) & DAT_0801ca5c;
        *(ushort *)((int)puVar1 + DAT_0801ca60) =
             (ushort)DAT_0801ca64 & *(ushort *)((int)puVar1 + DAT_0801ca60);
        *(byte *)((int)puVar1 + DAT_0801ca68) = *(byte *)((int)puVar1 + DAT_0801ca68) & 0x1f;
        *(byte *)(puVar1 + 0x488) = (byte)puVar1[0x488] & 0xf0;
        *pbVar4 = *pbVar4 & 0x80 | (*pbVar4 & 0x7f) + 1 & 0x7f;
        FUN_08010060(uVar3,0xc);
        FUN_0800a3e0(0,uVar3 + 4);
        return in_lr;
      }
    }
    else if (bVar2 == 10) {
      if (-1 < (int)((uint)*(byte *)(DAT_0801cae0 + DAT_0801cae4) * 0x2000000)) {
        return in_lr;
      }
      bVar2 = (byte)DAT_0801c9d4[0x488] & 0xdf;
      goto LAB_0801caf6;
    }
    bVar2 = (byte)DAT_0801c9d4[0x488] & 0xdf;
  }
LAB_0801caf6:
  *(byte *)(DAT_0801c9d4 + 0x488) = bVar2;
  return in_lr;
}



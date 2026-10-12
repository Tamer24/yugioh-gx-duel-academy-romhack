// ===== 080268C0 FUN_080268c0

undefined4 FUN_080268c0(void)

{
  byte bVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  byte *pbVar5;
  undefined4 in_lr;
  undefined2 local_20;
  undefined1 auStack_1e [18];
  
  iVar3 = DAT_08026954;
  iVar2 = DAT_0802694c;
  pbVar5 = (byte *)(DAT_0802694c + DAT_08026950);
  bVar1 = *pbVar5;
  *(undefined1 *)(DAT_0802694c + DAT_08026954) = 0;
  *(undefined1 *)(iVar2 + iVar3 + 1) = 0;
  *pbVar5 = bVar1 & 0xf6 | 2;
  if ((((bVar1 & 4) != 0) && ((*(byte *)(DAT_08026958 + 0x208) & 8) != 0)) &&
     (uVar4 = (*(uint *)(iVar2 + DAT_0802695c) & 0x3ffff) >> 0xc, uVar4 != 3)) {
    local_20 = (undefined2)uVar4;
    load_data_in_word_chuncks(auStack_1e,iVar2 + DAT_08026960,0x10);
    FUN_08026f30(DAT_08026964,&local_20,0x12);
    *(byte *)(DAT_08026968 + DAT_0802696c) = *(byte *)(DAT_08026968 + DAT_0802696c) & 0xfe;
    *pbVar5 = *pbVar5 | 1;
  }
  return in_lr;
}



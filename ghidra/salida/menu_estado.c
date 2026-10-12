// ===== 08026614 FUN_08026614

undefined8 FUN_08026614(void)

{
  undefined4 uVar1;
  uint uVar2;
  byte *pbVar3;
  undefined4 in_lr;
  undefined8 uVar4;
  
  if ((*(byte *)(DAT_0802662c + DAT_08026630) & 2) != 0) {
    if ((*(byte *)(DAT_0802662c + DAT_08026630) & 5) == 5) {
      if ((*(byte *)(DAT_0802664c + DAT_08026650) & 1) != 0) {
        pbVar3 = (byte *)(DAT_080268b8 + DAT_080268b4);
        if ((*pbVar3 & 5) == 1) {
          FUN_08026f30(DAT_080268bc,DAT_080268b8 + DAT_080268b4 + 0x15,0x10);
        }
        *pbVar3 = *pbVar3 & 0xfd;
        FUN_0801f4c0();
      }
      uVar1 = 1;
      goto LAB_080268ae;
    }
    uVar2 = ((*(uint *)(DAT_0802662c + DAT_08026670) & 0x3ffff) >> 0xc) - 1;
    if (uVar2 < 0x1d) {
                    /* WARNING: Could not recover jumptable at 0x0802666c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      uVar4 = (**(code **)(uVar2 * 4 + DAT_08026674))();
      return uVar4;
    }
  }
  uVar1 = 0;
LAB_080268ae:
  return CONCAT44(in_lr,uVar1);
}


// ===== 080269D0 FUN_080269d0

undefined4 FUN_080269d0(byte param_1,uint param_2,undefined4 param_3,int param_4)

{
  int iVar1;
  uint *puVar2;
  undefined4 in_lr;
  
  iVar1 = DAT_08026a28;
  if (8 < param_4) {
    param_4 = 8;
  }
  *(byte *)(DAT_08026a28 + DAT_08026a2c) =
       *(byte *)(DAT_08026a28 + DAT_08026a2c) & 0xfb | (param_1 & 1) << 2;
  puVar2 = (uint *)(iVar1 + DAT_08026a30);
  *puVar2 = *puVar2 & DAT_08026a34 | (param_2 & 0x3f) << 0xc;
  load_data_in_word_chuncks(iVar1 + DAT_08026a38,param_3,param_4 << 1);
  FUN_080268c0();
  return in_lr;
}



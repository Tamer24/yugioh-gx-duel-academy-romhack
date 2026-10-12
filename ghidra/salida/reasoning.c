// ===== 08046B80 FUN_08046b80

void FUN_08046b80(byte *param_1)

{
  undefined4 uVar1;
  code *UNRECOVERED_JUMPTABLE;
  
  if (((param_1[2] & 8) == 0) && (*(char *)(iRam08046ba0 + iRam08046ba4) == -0x80)) {
    FUN_08026970(1 - (*param_1 & 1),9,0,0);
    uVar1 = 0x7f;
  }
  else {
    uVar1 = 0;
  }
                    /* WARNING: Could not recover jumptable at 0x08046bc0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(uVar1);
  return;
}


// ===== 08035244 FUN_08035244

void FUN_08035244(byte *param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 uVar2;
  code *UNRECOVERED_JUMPTABLE;
  
  if ((((*(ushort *)(iRam08035284 * -((int)((uint)*param_1 << 0x1f) >> 0x1f) + iRam08035280 + 0x1c)
        & 0x1fff) >> 6 == 0) || (iVar1 = effect_activation_gatekeeper(param_1,param_2), iVar1 == 0))
     || (iVar1 = count_empty_field_slots(*param_1 & 1), iVar1 == 0)) {
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
  }
                    /* WARNING: Could not recover jumptable at 0x0803528e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(uVar2);
  return;
}



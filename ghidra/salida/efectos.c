// ===== 080577E8 state_machine_effect_resolution

longlong state_machine_effect_resolution(void)

{
  uint uVar1;
  code *UNRECOVERED_JUMPTABLE;
  uint in_lr;
  longlong lVar2;
  
  uVar1 = (*(uint *)(DAT_08057814 + 0x7c0) & 0x3ffff) >> 10;
  if (5 < uVar1) {
    return (ulonglong)in_lr << 0x20;
  }
  UNRECOVERED_JUMPTABLE = *(code **)(uVar1 * 4 + DAT_08057818);
                    /* WARNING: Could not recover jumptable at 0x08057812. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  lVar2 = (*UNRECOVERED_JUMPTABLE)(UNRECOVERED_JUMPTABLE,DAT_08057818,DAT_08057814);
  return lVar2;
}


// ===== 080317E4 effect_activation_gatekeeper

ulonglong effect_activation_gatekeeper(byte *param_1)

{
  undefined4 uVar1;
  undefined4 in_lr;
  
  uVar1 = check_player_can_activate_effects(*param_1 & 1);
  return CONCAT44(in_lr,uVar1) & 0xffffffff0000ffff;
}


// ===== 0803E3AC FUN_0803e3ac

undefined8 FUN_0803e3ac(byte *param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 in_lr;
  
  if ((param_1[2] & 8) == 0) {
    iVar2 = DAT_0803e3f4 * (1 - (*param_1 & 1)) + DAT_0803e3f0;
    if (((*(byte *)(iVar2 + 0x1c) & 0x3f) != 0 || *(char *)(iVar2 + 0x1b) < '\0') &&
       (iVar2 = FUN_08009094(0x10000), iVar2 == 0)) {
      uVar1 = 0x80;
      goto LAB_0803e3fa;
    }
  }
  uVar1 = 0;
LAB_0803e3fa:
  return CONCAT44(in_lr,uVar1);
}


// ===== 080616B8 FUN_080616b8

undefined8 FUN_080616b8(ushort *param_1,undefined2 param_2)

{
  int iVar1;
  uint uVar2;
  undefined4 in_lr;
  
  if (param_1 == (ushort *)0x0) {
    uVar2 = 0;
  }
  else {
    iVar1 = FUN_0806162c(*(ushort *)
                          (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_08061710 * ((*param_1 & 0x1ff) >> 8) + DAT_0806170c + 0x24) & 0x7fff)
    ;
    if ((iVar1 < 0) || (*(int *)(iVar1 * 0x1c + DAT_08061714 + 0xc) == 0)) {
      uVar2 = 1;
    }
    else {
      uVar2 = call_function_bx_r2(param_1,param_2);
      uVar2 = uVar2 & 0xffff;
    }
  }
  return CONCAT44(in_lr,uVar2);
}


// ===== 08051680 FUN_08051680

undefined8 FUN_08051680(byte *param_1,ushort param_2)

{
  undefined4 uVar1;
  undefined4 in_lr;
  
  if ((*param_1 & 1) == 0) {
    FUN_080e6d88(1);
  }
  uVar1 = 1;
  if ((*param_1 & 1) != 0) {
    uVar1 = DAT_080516c4;
  }
  drawing_FUN_08022034(uVar1,param_2,1);
  FUN_08051650(param_1,param_2 & 0xff);
  return CONCAT44(in_lr,1);
}


// ===== 0801A5BC FUN_0801a5bc

undefined4 FUN_0801a5bc(int param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4)

{
  undefined4 uVar1;
  undefined4 in_lr;
  
  uVar1 = 0x4b;
  if (param_1 != 0) {
    uVar1 = DAT_0801a5e0;
  }
  drawing_FUN_08021fe8(uVar1,param_2,param_3,param_4);
  return in_lr;
}


// ===== 0805A754 card_specific_effect_dispatcher

longlong card_specific_effect_dispatcher(int param_1)

{
  uint uVar1;
  longlong lVar2;
  
  if (((*(byte *)(param_1 + 2) & 8) == 0) &&
     (uVar1 = *(byte *)(DAT_0805a790 + DAT_0805a794) - 0x62, uVar1 < 0x1f)) {
                    /* WARNING: Could not recover jumptable at 0x0805a78a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    lVar2 = (**(code **)(uVar1 * 4 + DAT_0805a798))();
    return lVar2;
  }
  return (ulonglong)*(uint *)(&stack0x000001fc + DAT_0805a78c) << 0x20;
}



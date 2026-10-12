// ===== 08009744 ask_question

undefined4 ask_question(void)

{
  undefined4 in_lr;
  
  create_question();
  drawing_FUN_08095080();
  return in_lr;
}


// ===== 080875F4 init_effect_dialogue

undefined4 init_effect_dialogue(short param_1,uint param_2,uint param_3,ushort param_4)

{
  uint *puVar1;
  uint uVar2;
  undefined2 *puVar3;
  uint uVar4;
  int iVar5;
  byte *pbVar6;
  undefined4 in_lr;
  
  if (param_1 == 0) {
    fast_clear_memory(DAT_08087700,SUB_08087704);
    puVar1 = DAT_08087708;
    fast_clear_memory(DAT_08087708,0x30);
    uVar2 = DAT_08087710;
    uVar4 = *puVar1 & DAT_08087710 | (DAT_0808770c & param_2 & 0xffff) << 0xb;
    *puVar1 = uVar4;
    puVar1[1] = param_3;
    if (param_3 == 0) {
      *puVar1 = uVar4 & uVar2;
    }
    FUN_08085234();
    *(ushort *)(puVar1 + 2) =
         (ushort)DAT_08087718 & (ushort)puVar1[2] | param_4 & (ushort)DAT_08087714;
    puVar1[2] = puVar1[2] & DAT_0808771c | (uint)(param_4 >> 0xb) << 0xc;
    FUN_08086008(0);
    puVar3 = (undefined2 *)(DAT_08087720 + DAT_08087724);
    iVar5 = 9;
    do {
      *puVar3 = 10;
      puVar3 = puVar3 + 1;
      iVar5 = iVar5 + -1;
    } while (-1 < iVar5);
  }
  fast_clear_memory(DAT_08087728,8);
  *(byte *)(DAT_0808772c + 0x1f) = *(byte *)(DAT_0808772c + 0x1f) & 0xdf;
  iVar5 = DAT_08087720;
  *(byte *)(DAT_08087720 + DAT_08087730) = *(byte *)(DAT_08087720 + DAT_08087730) & 0x87 | 0x28;
  pbVar6 = (byte *)(iVar5 + DAT_08087734);
  *pbVar6 = *pbVar6 & 0xf0 | 4;
  pbVar6 = (byte *)(iVar5 + DAT_08087738);
  *pbVar6 = *pbVar6 & 0xf0 | 5;
  iVar5 = DAT_08087700;
  *(undefined4 *)(DAT_08087700 + DAT_0808773c) = DAT_08087740;
  *(undefined4 *)(iVar5 + DAT_08087744) = DAT_08087748;
  if ((DAT_0808774c & (ushort)DAT_08087708[2]) == 7) {
    FUN_080b8b58(5);
    *(byte *)(iVar5 + DAT_08087750) = *(byte *)(iVar5 + DAT_08087750) | 1;
    *(byte *)(iVar5 + DAT_08087754) = *(byte *)(iVar5 + DAT_08087754) & 0xc1;
  }
  else {
    FUN_080b8b58(4);
    *(byte *)(iVar5 + DAT_0808777c) = *(byte *)(iVar5 + DAT_0808777c) & 0xc1 | 2;
  }
  return in_lr;
}



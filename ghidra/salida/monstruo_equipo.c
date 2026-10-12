// ===== 08061A74 card_effect_handler_draw_11cards

undefined8 card_effect_handler_draw_11cards(ushort *param_1)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  int iVar4;
  short sVar5;
  uint uVar6;
  uint uVar7;
  int iVar8;
  int iVar9;
  undefined4 uVar10;
  int iVar11;
  undefined4 in_lr;
  
  uVar7 = DAT_08061c60;
  uVar6 = (*(byte *)((int)param_1 + 1) & 0x1f) >> 1;
  if (uVar6 == 3) {
    bVar1 = *(byte *)(DAT_08061aac + DAT_08061ab0);
    if (bVar1 == 0x7f) {
      uVar10 = 3;
      if ((*param_1 & 1) != 0) {
        uVar10 = DAT_08061b98;
      }
      drawing_FUN_08022084(uVar10,(*param_1 & 0x1ff) >> 1);
      uVar10 = 0x49;
      if ((*param_1 & 1) != 0) {
        uVar10 = DAT_08061b9c;
      }
      drawing_FUN_08021fe8(uVar10,(*param_1 & 0x1ff) >> 1,*(byte *)((int)param_1 + 9),1);
      uVar10 = 3;
      if ((*param_1 & 1) != 0) {
        uVar10 = DAT_08061b98;
      }
      drawing_FUN_08022084(uVar10,*(byte *)((int)param_1 + 9));
      uVar10 = 0x7e;
      goto FUN_08061cfc;
    }
    if (bVar1 < 0x80) {
      if (bVar1 == 0x7e) {
        iVar8 = FUN_08010c78(0,DAT_08061c60,0xff);
        iVar9 = FUN_08010c78(1,uVar7,0xff);
        iVar4 = DAT_08061c68;
        iVar3 = SUB_08061c64;
        if (0 < iVar8 + iVar9) {
          iVar11 = 0;
          do {
            uVar6 = FUN_0800e6a0((byte)*param_1 & 1,5,iVar11);
            if ((uVar6 != 0xff) &&
               (*(ushort *)
                 ((*(ushort *)
                    ((uVar6 & 0x7f) * 0x50 + DAT_08061c6c * ((int)(uVar6 & 0x80) >> 7) + iVar4 +
                    0x24) & 0x7fff) * 2 + iVar3) == uVar7)) {
              FUN_0801aaa4((byte)*param_1 & 1,uVar6);
              break;
            }
            iVar11 = iVar11 + 1;
          } while (iVar11 < 5);
          FUN_0801ad6c((*(uint *)(((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                  DAT_08061c6c * ((*param_1 & 0x1ff) >> 8) + DAT_08061c68 + 0x30) &
                       0xfffff) >> 0x13,(iVar8 + iVar9) * 1000);
        }
      }
    }
    else if (((bVar1 == 0x80) && ((param_1[4] & 0xf) != 0)) &&
            (sVar5 = FUN_080617ec((byte)*param_1 & 1,(*param_1 & 0x1ff) >> 1,
                                  *(byte *)((int)param_1 + 9)), sVar5 != 0)) {
      uVar10 = 0x3c;
      if ((*param_1 & 1) != 0) {
        uVar10 = DAT_08061b40;
      }
      drawing_FUN_08022034(uVar10,(*param_1 & 0x1ff) >> 1,0x13);
      uVar2 = *param_1;
      uVar7 = FUN_08011120((byte)*param_1 & 1);
      FUN_080188ac((uVar2 & 0x1ff) >> 1,
                   ((byte)*param_1 & 1) << 0xf | (uVar7 & 0x3f) << 4 | 0x1400 | 8);
      FUN_08019884((*param_1 & 0x1ff) >> 1);
      uVar10 = 0x7f;
      goto FUN_08061cfc;
    }
  }
  else if ((uVar6 == 6) && (((byte)param_1[1] & 8) == 0)) {
    bVar1 = *(byte *)(DAT_08061c94 + DAT_08061c98);
    if (bVar1 == 0x7f) {
      record_monster_summon((byte)*param_1 & 1,(*param_1 & 0x1ff) >> 1,0,1,(byte)param_1[1] & 8);
      uVar10 = 0x7e;
      goto FUN_08061cfc;
    }
    if (bVar1 < 0x80) {
      if (bVar1 == 0x7e) {
        uVar10 = 0x3c;
        if ((*param_1 & 1) != 0) {
          uVar10 = DAT_08061d0c;
        }
        drawing_FUN_08022034(uVar10,(*param_1 & 0x1ff) >> 1,0x13);
      }
    }
    else if (bVar1 == 0x80) {
      uVar10 = 0x4c;
      if ((*param_1 & 1) != 0) {
        uVar10 = DAT_08061cc0;
      }
      drawing_FUN_08022084(uVar10,(*param_1 & 0x1ff) >> 1);
      uVar10 = 0x7f;
      goto FUN_08061cfc;
    }
  }
  uVar10 = 0;
FUN_08061cfc:
  return CONCAT44(in_lr,uVar10);
}


// ===== 0803C038 FUN_0803c038

longlong FUN_0803c038(ushort *param_1)

{
  byte bVar1;
  ushort uVar2;
  undefined4 uVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  uint in_lr;
  longlong lVar8;
  
  uVar4 = (uint)*param_1;
  bVar1 = *(byte *)(((uVar4 & 0x1ff) >> 1 & 0x7f) * 0x50 + ((uVar4 & 0x1ff) >> 8) * DAT_0803c104 +
                    DAT_0803c100 + 0x3c);
  uVar6 = (uint)bVar1;
  if (((param_1[1] & 8) == 0) && (uVar6 != 0xff)) {
    iVar7 = (uVar6 & 0x7f) * 0x50 + (uint)(bVar1 >> 7) * DAT_0803c104;
    iVar5 = iVar7 + DAT_0803c100;
    if ((((*(uint *)(iVar5 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0) &&
       ((int)((uint)*(byte *)(iVar5 + 0x33) * 0x8000000) < 0)) {
      uVar4 = (uint)*(ushort *)
                     ((*(ushort *)
                        (((uVar4 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         ((uVar4 & 0x1ff) >> 8) * DAT_0803c104 + DAT_0803c100 + 0x24) & 0x7fff) * 2
                     + DAT_0803c108);
      if (uVar4 == DAT_0803c10c) {
        cleanup_card_actions();
        lVar8 = send_card_to_graveyard(uVar6,0x41,(*param_1 & 0x1ff) >> 1);
        return lVar8;
      }
      if (uVar4 == DAT_0803c10c + 0xea) {
        uVar2 = *param_1;
        uVar3 = FUN_080e22ec(*(undefined4 *)(iVar7 + DAT_0803c100 + 0x28));
        FUN_0801ad6c(-((int)((uint)(byte)uVar2 << 0x1f) >> 0x1f),uVar3);
      }
    }
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 0803BE9C FUN_0803be9c

longlong FUN_0803be9c(ushort *param_1)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  uint in_lr;
  longlong lVar4;
  
  iVar1 = FUN_08011120((byte)*param_1 & 1);
  if ((param_1[1] & 8) == 0) {
    FUN_08018850((*param_1 & 0x1ff) >> 1);
    iVar2 = FUN_080295e4(param_1,*(byte *)((int)param_1 + 9));
    if ((iVar2 != 0) && (iVar1 != -1)) {
      uVar3 = (uint)*param_1;
      if (-1 < (int)((uint)*(byte *)(((uVar3 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                     DAT_0803bf3c * ((uVar3 & 0x1ff) >> 8) + DAT_0803bf38 + 0x33) *
                    0x8000000)) {
        cleanup_card_actions();
        lVar4 = send_card_to_graveyard
                          (*(byte *)((int)param_1 + 9),((byte)*param_1 & 1) << 0xf | 0x41,
                           (*param_1 & 0x1ff) >> 1);
        return lVar4;
      }
      if (((*(uint *)(((uVar3 & 0x1ff) >> 1 & 0x7f) * 0x50 + DAT_0803bf3c * ((uVar3 & 0x1ff) >> 8) +
                      DAT_0803bf38 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0) {
        cleanup_card_actions();
        lVar4 = send_card_to_graveyard(*(byte *)((int)param_1 + 9),0,(*param_1 & 0x1ff) >> 1);
        return lVar4;
      }
      cleanup_card_actions();
      lVar4 = send_card_to_graveyard
                        (*(byte *)((int)param_1 + 9),((byte)*param_1 & 1) << 0xf | 0x41,
                         (*param_1 & 0x1ff) >> 1);
      return lVar4;
    }
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 080110DC FUN_080110dc

undefined8 FUN_080110dc(int param_1,uint param_2)

{
  char *pcVar1;
  int iVar2;
  uint uVar3;
  undefined4 in_lr;
  
  uVar3 = 0x20;
  iVar2 = 5;
  pcVar1 = (char *)(DAT_08011104 + param_1 * 0xb + DAT_08011108);
  while ((*pcVar1 != -1 || ((param_2 & uVar3) != 0))) {
    uVar3 = uVar3 << 1;
    pcVar1 = pcVar1 + 1;
    iVar2 = iVar2 + 1;
    if (9 < iVar2) {
      iVar2 = -1;
LAB_0801111a:
      return CONCAT44(in_lr,iVar2);
    }
  }
  iVar2 = iVar2 + -5;
  goto LAB_0801111a;
}


// ===== 08011074 FUN_08011074

undefined8 FUN_08011074(int param_1,uint param_2)

{
  char *pcVar1;
  uint uVar2;
  uint uVar3;
  undefined4 in_lr;
  
  uVar3 = 1;
  uVar2 = 0;
  pcVar1 = (char *)(param_1 * 0xb + DAT_080110b8 + DAT_080110c0);
  do {
    if (((*pcVar1 == -1) && ((param_2 & uVar3) == 0)) &&
       (((int)(*(byte *)(DAT_080110bc * param_1 + DAT_080110b8 + DAT_080110c4) & 0x1f) >>
         (uVar2 & 0xff) & 1U) == 0)) goto LAB_080110d6;
    uVar3 = uVar3 << 1;
    pcVar1 = pcVar1 + 1;
    uVar2 = uVar2 + 1;
  } while ((int)uVar2 < 5);
  uVar2 = 0xffffffff;
LAB_080110d6:
  return CONCAT44(in_lr,uVar2);
}



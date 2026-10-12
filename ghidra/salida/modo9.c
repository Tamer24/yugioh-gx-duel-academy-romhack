// ===== 0806A8D4 FUN_0806a8d4

undefined4 FUN_0806a8d4(void)

{
  return 1;
}


// ===== 0806A8D8 FUN_0806a8d8

undefined8 FUN_0806a8d8(void)

{
  char cVar1;
  char *pcVar2;
  undefined4 in_lr;
  
  pcVar2 = (char *)(DAT_0806a8f8 + DAT_0806a8fc);
  cVar1 = *pcVar2;
  if (cVar1 == '\0') {
    ask_multiple(DAT_0806a92c,DAT_0806a92c + DAT_0806a930,DAT_0806a92c + DAT_0806a934,
                 DAT_0806a92c + DAT_0806a930 + 0xae);
    *pcVar2 = *pcVar2 + '\x01';
  }
  else {
    *(undefined2 *)(DAT_0806a8f8 + DAT_0806a908) = *(undefined2 *)(DAT_0806a900 + DAT_0806a904);
  }
  return CONCAT44(in_lr,(uint)(cVar1 != '\0'));
}



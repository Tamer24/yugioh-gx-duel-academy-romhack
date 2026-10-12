// ===== 08042FBC FUN_08042fbc

longlong FUN_08042fbc(byte *param_1)

{
  uint in_lr;
  
  if ((param_1[2] & 8) == 0) {
    FUN_0801abf0(1 - (*param_1 & 1),500);
  }
  return (ulonglong)in_lr << 0x20;
}



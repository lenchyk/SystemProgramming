section .data
fmt: db "%s%f  s=%d",10,0
str1: db "b=",0
b times 4 db 0
a times 20 db 0
n times 1 db 0
s times 1 db 0
@buff1 db 0
@buff2 db 0
@buff3 db 0
@buff4 db 0

section .text
extern printf
global main

main: push rbp
mov rbp, rsp
xorps xmm2,xmm2

; 2

mov dword [@buff1], 0x0
movss xmm4, dword [@buff1]

movss dword [b], xmm4

; 3

mov al, 0

movzx eax, al
mov byte [s], al

; 4

mov al, 2

movzx eax, al
mov byte [n], al

; 5

mov dword [@buff1], 0x3f800000
movss xmm4, dword [@buff1]
mov al, 0
movsx   eax, al
cdqe

movss dword [a + rax*4], xmm4

; 6

mov dword [@buff1], 0x40200000
movss xmm1, dword [@buff1]
xorps xmm0, xmm0
subss xmm0, xmm1
movss xmm5, xmm0
movss xmm4, xmm5
mov al, 1
movsx   eax, al
cdqe

movss dword [a + rax*4], xmm4

; 7

mov dword [@buff1], 0x40400000
movss xmm4, dword [@buff1]
mov al, 2
movsx   eax, al
cdqe

movss dword [a + rax*4], xmm4

; 8

mov dword [@buff1], 0x40933333
movss xmm4, dword [@buff1]
mov al, 3
movsx   eax, al
cdqe

movss dword [a + rax*4], xmm4

; 9

mov dword [@buff1], 0x40e00000
movss xmm4, dword [@buff1]
mov al, 4
movsx   eax, al
cdqe

movss dword [a + rax*4], xmm4

; 10


movzx eax, byte [n]
sub eax, 1
mov byte [n], al
movsx   eax, byte [n]
cdqe

movss xmm0, dword [a + rax*4]

movss xmm1, dword [b]
addss xmm0, xmm1
movss xmm6, xmm0
movss xmm4, xmm6

movss dword [b], xmm4
movss xmm0, dword [b]
cvtss2sd xmm1,xmm0
movsd xmm0,xmm1
mov rdi,fmt
mov rsi,str1
xor rdx,rdx
movzx edx, byte [s]
mov rax,1
call printf
mov rsp,rbp
pop rbp
mov rax,0
ret
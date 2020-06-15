# torch.nn.Conv2d

```python
torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True, padding_mode='zeros')
```



```python
in = torch.randn(20, 16, 50, 100)  # 输入为[batch_size, channels, height_in, width_in]
m = nn.Conv2d(16, 33, (3, 5), stride=(2, 1), padding=(4, 2))
out = m(in)
out.shape # 输出为[batch_size, output, height_out, width_out]
# torch.Size([20, 33, 28, 100])
```


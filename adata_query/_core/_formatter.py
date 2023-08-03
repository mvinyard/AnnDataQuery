
# -- import packages: ----------------------------------------------------------
import ABCParse
import autodevice
import anndata
import numpy as np
import torch as _torch


# -- set typing: ---------------------------------------------------------------
from typing import Union


# -- operational class: --------------------------------------------------------
class DataFormatter(ABCParse.ABCParse):
    def __init__(self, data: Union[_torch.Tensor, np.ndarray], *args, **kwargs):
        self.__parse__(locals())

    @property
    def device_type(self) -> str:
        """Returns device type"""
        if hasattr(self.data, "device"):
            return self.data.device.type
        return "cpu"

    @property
    def is_ArrayView(self) -> bool:
        """Checks if device is of type ArrayView"""
        return isinstance(self.data, anndata._core.views.ArrayView)

    @property
    def is_numpy_array(self) -> bool:
        """Checks if device is of type np.ndarray"""
        return isinstance(self.data, np.ndarray)

    @property
    def is_torch_Tensor(self) -> bool:
        """Checks if device is of type torch.Tensor"""
        return isinstance(self.data, _torch.Tensor)

    @property
    def on_cpu(self) -> bool:
        """Checks if device is on cuda or mps"""
        return self.device_type == "cpu"

    @property
    def on_gpu(self) -> bool:
        """Checks if device is on cuda or mps"""
        return self.device_type in ["cuda", "mps"]

    def to_numpy(self) -> np.ndarray:
        """Sends data to np.ndarray"""
        if self.is_torch_Tensor:
            if self.on_gpu:
                return self.data.detach().cpu().numpy()
            return self.data.numpy()
        elif self.is_ArrayView:
            return self.data.toarray()
        return self.data

    def to_torch(self, device=autodevice.AutoDevice()) -> _torch.Tensor:
        """
        Parameters
        ----------
        device: torch.device

        Returns
        -------
        torch.Tensor
        """
        self.__update__(locals())

        if self.is_torch_Tensor:
            return self.data.to(device)
        elif self.is_ArrayView:
            self.data = self.data.toarray()
        return _torch.Tensor(self.data).to(device)


# -- functional wrap: ----------------------------------------------------------
def format_data(data: Union[np.ndarray, _torch.Tensor], torch: bool = False, device: _torch.device = autodevice.AutoDevice()):
    
    formatter = DataFormatter(data=data)
    if torch:
        return formatter.to_torch(device=device)
    return formatter.to_numpy()
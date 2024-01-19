
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
    """DataFormatter cls"""
    def __init__(self, data: Union[_torch.Tensor, np.ndarray], *args, **kwargs) -> None:
        """Format data to interface with numpy or torch, on a specified device.

        Args:
            data (``Union[np.ndarray, torch.Tensor]``): Input ``data`` to be formatted. Typically an ``np.ndarray``, ``torch.Tensor``, or ``ArrayView``.

        Returns:
            None
        """
        self.__parse__(locals())

    @property
    def device_type(self) -> str:
        """Returns device type
        """
        if hasattr(self._data, "device"):
            return self._data.device.type
        return "cpu"

    @property
    def is_ArrayView(self) -> bool:
        """Checks if device is of type ArrayView"""
        return isinstance(self._data, anndata._core.views.ArrayView)

    @property
    def is_numpy_array(self) -> bool:
        """Checks if device is of type np.ndarray"""
        return isinstance(self._data, np.ndarray)

    @property
    def is_torch_Tensor(self) -> bool:
        """Checks if device is of type torch.Tensor"""
        return isinstance(self._data, _torch.Tensor)

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
                return self._data.detach().cpu().numpy()
            return self._data.numpy()
        elif self.is_ArrayView:
            return self._data.toarray()
        return self._data

    def to_torch(self, device: _torch.device = autodevice.AutoDevice()) -> _torch.Tensor:
        """Description of function.

        Args:
            device (``Optional[torch.device]``): If ``torch==True``, the device (e.g.: ``"cpu"``, ``"cuda:0"``, ``"mps:0"``) may be set. The default value, ``autodevice.AutoDevice()`` will indicate the use of GPU, if available.
            
            - **Default**: ``autodevice.AutoDevice()``

        Returns:
            ``Union[np.ndarray, torch.Tensor]``: ``formatted_data``
        """
        self.__update__(locals())

        if self.is_torch_Tensor:
            return self._data.to(self._device)
        elif self.is_ArrayView:
            self._data = self._data.toarray()
        return _torch.Tensor(self._data).to(self._device)


# -- functional wrap: ----------------------------------------------------------
def format_data(
    data: Union[np.ndarray, _torch.Tensor], 
    torch: bool = False, 
    device: _torch.device = autodevice.AutoDevice(),
) -> Union[np.ndarray, _torch.Tensor]:
    """Format data to interface with numpy or torch, on a specified device.

    Args:
        data (``Union[np.ndarray, torch.Tensor]``): Input ``data`` to be formatted. Typically an ``np.ndarray``, ``torch.Tensor``, or ``ArrayView``.
    
        torch (``Optional[bool]``): Toggle whether data should be formatted as ``torch.Tensor`` or ``np.ndarray``.
        
            - **Default**: ``False``
            
        device (``Optional[torch.device]``): If ``torch==True``, the device (e.g.: ``"cpu"``, ``"cuda:0"``, ``"mps:0"``) may be set. The default value, ``autodevice.AutoDevice()`` will indicate the use of GPU, if available.
            
            - **Default**: ``autodevice.AutoDevice()``

    Returns:
        ``Union[np.ndarray, torch.Tensor]``: ``formatted_data``
    """
    formatter = DataFormatter(data=data)
    
    if torch:
        return formatter.to_torch(device=device)
    return formatter.to_numpy()

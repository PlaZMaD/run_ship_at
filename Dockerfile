FROM conda/miniconda3
WORKDIR /run_ship_at
COPY requirements.txt /run_ship_at/requirements.txt
RUN  pip install -r /run_ship_at/requirements.txt
COPY . /run_ship_at


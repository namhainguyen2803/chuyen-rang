weight_fsw_values=(0.5)
methods=(EFBSW FBSW lowerboundFBSW BSW)
obsw_weights=(0.1 1.0 10.0)
num_epochs=300
seed_id=28
batch_size=1000
batch_size_test=128
distribution="circle"
optimizer="rmsprop"
lr=0.001
saved_model_interval=50
alpha=0.9
datadir="data"
outdir="result"
weight_swd=8.0
gpu_id=1

for weight_fsw in "${weight_fsw_values[@]}"; do
    for lmbd in "${obsw_weights[@]}"; do
        CUDA_VISIBLE_DEVICES="$gpu_id" python3 train.py \
            --dataset mnist \
            --num-classes 10 \
            --datadir "$datadir" \
            --outdir "$outdir" \
            --distribution "$distribution" \
            --epochs "$num_epochs" \
            --optimizer "$optimizer" \
            --lr "$lr" \
            --alpha "$alpha" \
            --batch-size "$batch_size" \
            --batch-size-test "$batch_size_test" \
            --seed "$seed_id" \
            --weight_swd "$weight_swd" \
            --weight_fsw "$weight_fsw" \
            --method OBSW \
            --lambda-obsw "$lmbd" \
            --saved-model-interval "$saved_model_interval"
    done
done
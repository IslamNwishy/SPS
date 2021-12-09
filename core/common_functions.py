from core.models import Order, OrderProcess, PipelineNode
import subprocess
import os
from docx import Document


def gen_doc(docu, instance, map):
    doc = Document(docu.file.open())
    keys = map.keys()
    for p in doc.paragraphs:
        if any(key in p.text for key in keys):
            inline = p.runs
            for i in range(len(inline)):
                for ele in map:
                    if ele in inline[i].text:
                        text = inline[i].text.replace(ele, map[ele])
                        inline[i].text = text

    filename = "media/order_docs/" + \
        str(instance.pk) + "_" + str(docu.title) + ".docx"
    doc.save(filename)
    subprocess.run(["abiword", "--to=pdf", filename])
    os.remove(filename)
    return "order_docs/" + \
        str(instance.pk) + "_" + str(docu.title) + ".pdf"


def next_process(instance):
    order = instance.order
    if instance.pipeline_node.is_last():
        order.verdict = Order.accept
        order.completion = Order.on_delivery
    else:
        next_in_pipeline = instance.pipeline_node.next()
        new_instance = OrderProcess(
            order=order, pipeline_node=next_in_pipeline,checked_by= instance.checked_by)
        new_instance.save()
        order.current_node = new_instance.pipeline_node
    order.save()
    map = {
        "cName": order.org.title,
        "oName": order.contact_user.name,
        "oDate": str(order.create_date),
        "oPhone": order.org.phone,
        "oEmail": order.contact_user.name,
        "oEndtime": str(order.end_time),
        "oEndDate": str(order.end_date),
        "oType": order.type,
        "oTitle": order.title,
        "oID": str(order.pk),
        "oDetails": order.details,
        "oBudget": str(order.budget),
        "oCurrency": order.currency
    }
    doc = instance.pipeline_node.generates_document
    if doc:
        instance.generated_doc = gen_doc(doc, order, map)
        instance.save()


def prev_process(instance):
    order = instance.order
    if instance.pipeline_node.rejection_behaviour == PipelineNode.review:
        prev_instance = instance.pipeline_node.prev()
        new_instance = OrderProcess(
            order=order, pipeline_node=prev_instance, checked_by=instance.checked_by)
        new_instance.save()
        order.current_node = new_instance.pipeline_node
    else:
        order.verdict = Order.reject
    order.save()
